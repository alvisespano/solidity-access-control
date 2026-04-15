// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;


contract Example {
    address private owner;
    uint private supply;
    
    constructor(address _owner) {
        supply = 0;
        // does not initialize the owner state variables
    }

    function setOwner(address a) public {
        require(msg.sender == owner);   // owner state variable is uninitialized thus equals to address(0)
        owner = a;
    }
}