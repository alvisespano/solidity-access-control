// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;


contract Proxy {
    address public implementation;

    constructor(address _impl) {
        implementation = _impl;
    }

    fallback() external payable {
        (bool success,) = implementation.delegatecall(msg.data);
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
        payable(msg.sender).transfer(address(this).balance);
    }
}