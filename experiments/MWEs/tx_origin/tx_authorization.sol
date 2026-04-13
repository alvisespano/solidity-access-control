// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;


contract Example {
    address private owner;

    constructor() {
        owner = msg.sender;
    }

    function withdraw() public {
        require(tx.origin == owner); // vulnerable check
        payable(msg.sender).call{value: address(this).balance}("");
    }
}