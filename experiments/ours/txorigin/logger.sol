// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract PrivateDeposit
{
    mapping (address => uint) public balances;
        
    uint public minDeposit = 1 ether;
    address public owner;
    
    Log TransferLog;
    
	// the guard is wrong and anyone can call the setLog() to change the current logger
    modifier onlyOwner() {
        require(tx.origin == owner);
        _;
    }    
    
    constructor() {
        owner = msg.sender;
        TransferLog = new Log();
    }
    
    function setLog(address _lib) public onlyOwner {
        TransferLog = Log(_lib);
    }    
    
    function deposit() public payable {
        if(msg.value >= minDeposit) {
            balances[msg.sender] += msg.value;
            TransferLog.AddMessage(msg.sender,msg.value,"Deposit");
        }
    }
    
    receive() external payable {}
    
}

contract Log {
   
    struct Message
    {
        address Sender;
        string  Data;
        uint Val;
        uint  Time;
    }
    
    Message[] public History;
    
    Message LastMsg;
    
    function AddMessage(address _adr, uint _val, string memory _data)
    public
    {
        LastMsg.Sender = _adr;
        LastMsg.Time = block.timestamp;
        LastMsg.Val = _val;
        LastMsg.Data = _data;
        History.push(LastMsg);
    }
}