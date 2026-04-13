// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;


contract Example {
    address private owner;

    function privileged() public {
        require(msg.sender != owner); // logic inverted
        // privileged operation
        owner = msg.sender; // ownership can be taken by anyone calling this function
    }
}