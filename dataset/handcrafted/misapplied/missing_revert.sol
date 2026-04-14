// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;


contract Example {
    address private owner;
    bool flag = false;

    function privileged() public {
        if (msg.sender == owner) {
            // intended restriction, but no revert on failure
            flag = true; // privileged operation only executes if the sender is the owner
        }
        // privileged operation still executes
        owner = msg.sender; // ownership can be taken by anyone calling this function
    }
}