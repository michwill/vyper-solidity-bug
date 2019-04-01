pragma solidity ^0.5.3;

contract SolContract {
    uint256 private _var1;
    uint256 private _var2;

    constructor () public {
        _var1 = 0;
        _var2 = 0;
    }

    function testTrueAfter() public returns (bool) {
        _var1 = 5;
        return true;
    }

    function testFalseAfter() public returns (bool) {
        _var1 = 50;
        return false;
    }

    function testTrue() public returns (bool) {
        return true;
    }

    function testFalse() public returns (bool) {
        return false;
    }
}
