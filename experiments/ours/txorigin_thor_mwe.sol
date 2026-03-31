// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract Vulnerable {
    mapping(address => uint256) public balances;

    constructor() {
        balances[msg.sender] = 1000;
    }

    function transferTo(address to, uint256 amount) public {
        require(balances[tx.origin] >= amount, "Not enough");

        balances[tx.origin] -= amount;
        balances[to] += amount;
    }
}