// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;


contract Vulnerable {
    mapping(address => uint256) public balances;
    
    constructor() {
        
    }

    function withdraw() public {
        require(balances[msg.sender] > 0, "No balance to withdraw");
        uint256 amount = balances[msg.sender]; // sload mstore
        balances[msg.sender] = 10; //sstore
        (bool success, ) = msg.sender.call{value: amount}(""); //mload
        require(success, "Transfer failed");

    }
}