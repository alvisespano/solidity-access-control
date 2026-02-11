// SPDX-License-Identifier: MIT 
pragma solidity ^0.8.30;

import "@openzeppelin/contracts/access/AccessControl.sol";

/*abstract contract MyAccessControl is Context, IAccessControl, ERC165 {

    bytes32 public constant DEFAULT_ADMIN_ROLE = 0x00;
    
    struct RoleData {
        mapping(address account => bool) hasRole;
        bytes32 adminRole;
    }

    mapping(bytes32 role => RoleData) private _roles;

    function hasRole(bytes32 role, address account) public view virtual returns (bool) {
        return _roles[role].hasRole[account];
    }

    function grantRole(bytes32 role, address account) public virtual onlyRole(getRoleAdmin(role)) {
        _grantRole(role, account);
    }

    function _grantRole(bytes32 role, address account) internal virtual returns (bool) {
        if (!hasRole(role, account)) {
            _roles[role].hasRole[account] = true;
            emit RoleGranted(role, account, _msgSender());
            return true;
        } else {
            return false;
        }
    }

    function revokeRole(bytes32 role, address account) public virtual onlyRole(getRoleAdmin(role)) {
        _revokeRole(role, account);
    }

    function _revokeRole(bytes32 role, address account) internal virtual returns (bool) {
        if (hasRole(role, account)) {
            _roles[role].hasRole[account] = false;
            emit RoleRevoked(role, account, _msgSender());
            return true;
        } else {
            return false;
        }
    }
    
    modifier onlyRole(bytes32 role) {
        _checkRole(role);
        _;
    }
}*/


contract MyHotel is AccessControl {

    bytes32 public constant DIRECTOR_ROLE = keccak256("DIRECTOR_ROLE");
	bytes32 public constant RECEPTIONIST_ROLE = keccak256("RECEPTIONIST_ROLE");
	bytes32 public constant HOUSEKEEPING_ROLE = keccak256("HOUSEKEEPING_ROLE");

	constructor(address admin) {
        _grantRole(DEFAULT_ADMIN_ROLE, admin);
        _setRoleAdmin(RECEPTIONIST_ROLE, DIRECTOR_ROLE);
        _setRoleAdmin(HOUSEKEEPING_ROLE, DIRECTOR_ROLE);
    }

    error NotAllowed(address, bytes32);

    function bookRoom() public {
        // anyone can call this bookRoom()
    }

    modifier onlyRoleWithError(bytes32 role) {
        if (!hasRole(role, _msgSender())) 
            revert NotAllowed(_msgSender(), role);
    	_;
    }

    function useReceptionistComputer() public { }

    function confirmRoom() public onlyRoleWithError(RECEPTIONIST_ROLE) {
        useReceptionistComputer();
    }

    function cleanRoom() public onlyRoleWithError(HOUSEKEEPING_ROLE) {
        // ... logic to confirm that a room is ready after cleaning
    }

   /*function fireHumanResource() public virtual onlyRole(getRoleAdmin(role)) {
   }*/
}

