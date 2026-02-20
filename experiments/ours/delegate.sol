pragma solidity ^0.8.30;


contract E {
    uint field;
    address a;

    constructor (address _a) {
        a = _a;
    }

    modifier guardia() {
        if(msg.sender == a)
            revert();
        _;
    }

    function sticazzi(uint n) guardia external { 
        selfdestruct();
     }
}
