// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.4.22;


contract MyContract {
    address private owner;
    
    MyContrac(address _owner) public { // typo in the constructor name
        owner = _owner;
    }
}