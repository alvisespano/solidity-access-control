/*
 * @source: https://smartcontractsecurity.github.io/SWC-registry/docs/SWC-124#arbitrary-location-write-simplesol
 * @author: Suhabe Bugrara
 * @vulnerable_at_lines: 27
 */

 pragma solidity ^0.8.30;

 contract C {

	function add1(uint x) internal pure returns (uint) {
		return x + 1;
	}

	function g1(function (uint) internal returns (uint) f) internal {
		uint r = f(7);

	}

	function g2(function (uint) external returns (uint) f) internal {
		uint r = f(7);

	}

	function g3(function (uint) internal returns (uint) f) internal {
		uint r = f(7);

	}

	function main() public {
		g(add1);
	}
 }
