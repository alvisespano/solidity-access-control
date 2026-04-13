// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;


contract Vulnerable {
    address private owner;
    uint private supply;
    
    constructor() {
        supply = 0;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    } 

    function setOwner(address _owner) onlyOwner public {
        owner = _owner;
    }
}