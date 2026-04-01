// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;


contract Parent {
    bool initialized = false;
	uint parentSupply;

    modifier initializer() {
        require(initialized == false, "Already initialized");
        initialized = true;
        _;
    }

    // can be executed only once
    function initializeParent() public initializer {
		parentSupply = 0;
    }
}

contract Child is Parent {
	uint childSupply;

	function initializeChild() public initializer {	
		super.initializeParent();	// the modifier of the parent fails
		childSupply = 0;
    }
}