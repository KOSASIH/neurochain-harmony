pragma solidity ^0.8.0;

import "https://github.com/OpenZeppelin/openzeppelin-solidity/contracts/token/ERC20/SafeERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-solidity/contracts/math/SafeMath.sol";
import "https://github.com/OpenZeppelin/openzeppelin-solidity/contracts/utils/Address.sol";

contract NeuroChainToken {
    using SafeMath for uint256;
    using SafeERC20 for address;

    // Token details
    string public name = "NeuroChain Token";
    string public symbol = "NCT";
    uint8 public decimals = 18;
    uint256 public totalSupply = 100000000 * (10 ** decimals);

    // Mapping of balances
    mapping (address => uint256) public balances;

    // Mapping of allowances
    mapping (address => mapping (address => uint256)) public allowances;

    // Event emitted when tokens are transferred
    event Transfer(address indexed from, address indexed to, uint256 value);

    // Event emitted when an approval is made
    event Approval(address indexed owner, address indexed spender, uint256 value);

    // Constructor function
    constructor() public {
        balances[msg.sender] = totalSupply;
    }

    // Transfer tokens from one address to another
    function transfer(address to, uint256 value) public returns (bool) {
        require(balances[msg.sender] >= value, "Insufficient balance");
        balances[msg.sender] = balances[msg.sender].sub(value);
        balances[to] = balances[to].add(value);
        emit Transfer(msg.sender, to, value);
        return true;
    }

    // Approve an address to spend tokens on behalf of another address
    function approve(address spender, uint256 value) public returns (bool) {
        allowances[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }

    // Transfer tokens from one address to another using an approved allowance
    function transferFrom(address from, address to, uint256 value) public returns (bool) {
        require(allowances[from][msg.sender] >= value, "Insufficient allowance");
        require(balances[from] >= value, "Insufficient balance");
        balances[from] = balances[from].sub(value);
        balances[to] = balances[to].add(value);
        allowances[from][msg.sender] = allowances[from][msg.sender].sub(value);
        emit Transfer(from, to, value);
        return true;
    }

    // Get the balance of an address
    function balanceOf(address owner) public view returns (uint256) {
        return balances[owner];
    }

    // Get the allowance of an address for another address
    function allowance(address owner, address spender) public view returns (uint256) {
        return allowances[owner][spender];
    }
}
