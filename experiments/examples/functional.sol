

 pragma solidity ^0.8.30;

 contract C {

	function add1(uint x) internal pure returns (uint) {
		return x + 1;
	}

	function add2(uint x) external pure returns (uint) {
		return x + 1;
	}



	function g1(function (uint) internal pure returns (uint) f) internal {
		uint r = f(7);
	}

	function g2(function (uint) external returns (uint) f) internal {
		uint r = f(7);
	}

	// function g3(function (uint) internal returns (uint) f) external {
	// 	uint r = f(7);
	// }

	function g4(function (uint) external returns (uint) f) external {
		uint r = f(7);
	}

	function g5(function (uint) returns (uint) f) internal {
		uint r = f(7);
	}

	// function g6(function (uint) returns (uint) f) external {
	// 	uint r = f(7);
	// }

	function g7(function (uint) view returns (uint) f) view internal {
		uint r = f(7);
	}

	function main() public {
		g1(add1);
		g2(this.add2);
		this.g4(this.add2);
		g5(add1);
	}
 }

 contract D {

	address a;
	address d;

	constructor (address _a, address _d) {
		a = _a;
		d = _d;
	}

	function f(uint x) external pure returns (uint) {
		return 7;
	}

	function main() public {
		C(a).g4(this.f);	// si può passare una external di questo contratto
		C(a).g4(E(d).f);	// oppure di un altro
	}
}

contract E {

	function f(uint x) external pure returns (uint) {
		return 7;
	}

}