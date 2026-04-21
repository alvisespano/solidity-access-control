
// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v5.6.0) (access/AccessControl.sol)

pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/AccessControl.sol";

contract Example is AccessControl {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant ROLEADDER_ROLE = keccak256("ROLEADDER_ROLE");

    mapping (bytes32 => address[]) private members;     // track all members explicitly

    constructor() {
        _grantRole(ADMIN_ROLE, msg.sender);
        _grantRole(ROLEADDER_ROLE, msg.sender);
    }

    // anyone with ROLEADDER_ROLE can add arbitrary accounts
    function addMember(address account, bytes32 role) external onlyRole(ROLEADDER_ROLE) {
        grantRole(role, account);
        members[role].push(account); // unbounded growth
    }

    // admin tries to revoke all members
    function revokeAll(bytes32 role) external onlyRole(ADMIN_ROLE) {
        address[] storage roleMembers = members[role];
        for (uint256 i = 0; i < roleMembers.length; ++i) {  // DoS if array is too long
            if (hasRole(role, roleMembers[i])) {
                revokeRole(role, roleMembers[i]);
            }
        }
    }
}