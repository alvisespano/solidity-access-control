
 pragma solidity ^0.8.30;

 contract C {

	function map(uint[] storage src, bool[] storage dst, function (uint) external returns (bool) f) internal {
		for (uint i = 0; i < src.length; ++i)
			dst.push(f(src[i]));
	}

	function map(uint[] memory src, bool[] memory dst, function (uint) external returns (bool) f) internal {
		for (uint i = 0; i < src.length; ++i)
			dst[i] = f(src[i]);
	}

	function foldLeft(uint[] memory src, uint zero, function (uint, uint) external returns (uint) f) internal returns (uint) {
		uint acc = zero;
		for (uint i = 0; i < src.length; ++i)
			acc = f(src[i], acc);
		return acc;
	}
}

