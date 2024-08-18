pragma solidity ^0.8.0;

contract NeuroChainHarmonyToken {
    address private owner;
    uint public totalSupply;

    constructor() public {
        owner = msg.sender;
        totalSupply = 1000000;
    }

    function transfer(address recipient, uint amount) public {
        // Transfer tokens from one address to another
        require(msg.sender == owner, "Only the owner can transfer tokens");
        recipient.transfer(amount);
    }

    function balanceOf(address account) public view returns (uint) {
        // Return the token balance of an address
        return account.balance;
    }

    function mint(address account, uint amount) public {
        // Mint new tokens
        require(msg.sender == owner, "Only the owner can mint tokens");
        totalSupply += amount;
        account.transfer(amount);
    }

    function burn(address account, uint amount) public {
        // Burn tokens
        require(msg.sender == owner, "Only the owner can burn tokens");
        require(account.balance >= amount, "Insufficient balance");
        totalSupply -= amount;
        account.transfer(amount);
    }
}
