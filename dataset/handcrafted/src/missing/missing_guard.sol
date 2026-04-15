// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;


contract Example {
    address private owner;
    
    constructor(address _owner) {
        owner = _owner;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function privileged() public {  // modifier is missing
        owner = msg.sender;  // anyone can call this function and become the owner
    }
}