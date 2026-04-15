// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.4.22;


contract Proxy {
    address private implementation;

    constructor(address _impl) public {
        implementation = _impl;
    }

    function fallback() external payable {
        bool success = implementation.delegatecall(msg.data);
        require(success);
    }
}

contract WalletLibrary {
    address public owner;

    function initWallet(address _owner) public {
        owner = _owner; // unprotected initialization
    }

    function withdraw() public {
        require(msg.sender == owner);
        msg.sender.transfer(address(this).balance);
    }
}