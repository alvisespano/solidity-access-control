// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;


contract Vulnerable {
    address private owner;
    uint private supply;
    
    constructor(address _owner) {
        initialize(_owner);
    }

    function initialize(address _owner) public {
        owner = _owner;
        supply = 0;
    }
}