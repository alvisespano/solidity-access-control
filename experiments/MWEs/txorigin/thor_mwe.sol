// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract Vulnerable {
    mapping(address => uint256) public balances;

    constructor(uint _totalSupply) payable {
        balances[msg.sender] = _totalSupply;
    }

    function transferTo(address to, uint256 amount) public {
        _transfer(tx.origin, to, amount);
    }

    function _transfer(address from, address to, uint256 amount) internal {
        require(balances[from] >= amount, "Not enough");
        balances[from] -= amount;
        balances[to] += amount;
    }

}