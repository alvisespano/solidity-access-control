// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;


contract Example {
    address public owner;

    constructor(address _owner) {
        owner = _owner;
    }

    function delegate(address to) external payable {
        (bool success,) = to.delegatecall(msg.data);
        require(success);
    }
}