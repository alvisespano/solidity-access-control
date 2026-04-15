// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;


contract Example {
    address public owner;
    uint256 public supply;
    bool private initialized;

    function initialize(address _owner) public {
        //require(!initialized, "Already initialized"); forget to check if already initialized
        owner = _owner;
        supply = 100;
        initialized = true;
    }
}