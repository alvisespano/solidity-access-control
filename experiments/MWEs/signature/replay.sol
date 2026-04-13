// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;


contract Example {
    address public owner;

    function payWithSig(address to, uint amt, bytes32 hash, uint8 v, bytes32 r, bytes32 s) public {
        address signer = ecrecover(hash, v, r, s);
        require(signer == owner);
        (bool success, ) = to.call{value: amt}("");  // payment can be executed multiple times
        require(success);
    }
}