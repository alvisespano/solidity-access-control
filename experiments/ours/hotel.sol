// SPDX-License-Identifier: MIT 
pragma solidity ^0.8.30;

import "@openzeppelin/contracts/access/AccessControl.sol";

contract Hotel is AccessControl {

    bytes32 public constant DIRECTOR_ROLE = keccak256("DIRECTOR_ROLE");
	bytes32 public constant RECEPTIONIST_ROLE = keccak256("RECEPTIONIST_ROLE");
	bytes32 public constant HOUSEKEEPING_ROLE = keccak256("HOUSEKEEPING_ROLE");

	constructor(address admin) {
        // is the right pattern calling the internal inherited functions or the public stubs?
        _grantRole(DEFAULT_ADMIN_ROLE, admin);
        _setRoleAdmin(RECEPTIONIST_ROLE, DIRECTOR_ROLE);
        _setRoleAdmin(HOUSEKEEPING_ROLE, DIRECTOR_ROLE);
    }

    error NotAllowed(address, bytes32);

    function bookRoom() public {} // anyone can call this: but how do we know it needs a guard?

    modifier onlyRoleWithError(bytes32 role) {
        if (!hasRole(role, _msgSender())) 
            revert NotAllowed(_msgSender(), role);
    	_;
    }

    function useReceptionistComputer() public { }   // must have guard since it is called from a public method with a guard

    function confirmRoom() public onlyRoleWithError(RECEPTIONIST_ROLE) {
        useReceptionistComputer();  // public methods called by methods having a guard MUST have a guard on its own
    }

    function cleanRoom() public onlyRoleWithError(HOUSEKEEPING_ROLE) {
        // ... logic to confirm that a room is ready after cleaning
    }

   /*function fireHumanResource() public virtual onlyRole(getRoleAdmin(role)) {
   }*/
}

