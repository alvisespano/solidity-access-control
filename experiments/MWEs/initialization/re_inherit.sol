// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;


contract Parent {
    address public owner;
    bool internal initialized;

    function initialize(address _owner) public {
        // missing check of the initialized flag
        owner = _owner;
        initialized = true;
    }
}

contract Derived is Parent {
    uint256 public supply;

    function initializeDerived(uint256 _supply, address _owner) public {
        super.initialize(_owner);
        supply = _supply;
    }
}