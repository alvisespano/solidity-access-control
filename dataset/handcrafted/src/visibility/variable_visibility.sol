// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;


contract SecretStore {
    uint public secretNum = 42;    // this should be private

    function guess(uint x) external {
        if (x == secretNum) {
            (bool success, ) = msg.sender.call{value: 1000}("");
        }
    }
}