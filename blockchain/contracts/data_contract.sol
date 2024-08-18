pragma solidity ^0.8.0;

import "https://github.com/OpenZeppelin/openzeppelin-solidity/contracts/token/ERC20/SafeERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-solidity/contracts/math/SafeMath.sol";

contract DataContract {
    using SafeERC20 for address;
    using SafeMath for uint256;

    // Mapping of data providers to their respective data
    mapping (address => mapping (string => bytes)) public dataProviders;

    // Mapping of data consumers to their respective data requests
    mapping (address => mapping (string => bytes)) public dataConsumers;

    // Event emitted when a new data provider is registered
    event NewDataProvider(address indexed provider, string dataId);

    // Event emitted when a new data consumer is registered
    event NewDataConsumer(address indexed consumer, string dataId);

    // Event emitted when a data request is made
    event DataRequest(address indexed consumer, string dataId);

    // Event emitted when data is updated
    event DataUpdate(address indexed provider, string dataId, bytes data);

    // Function to register a new data provider
    function registerDataProvider(string memory _dataId) public {
        dataProviders[msg.sender][_dataId] = "";
        emit NewDataProvider(msg.sender, _dataId);
    }

    // Function to register a new data consumer
    function registerDataConsumer(string memory _dataId) public {
        dataConsumers[msg.sender][_dataId] = "";
        emit NewDataConsumer(msg.sender, _dataId);
    }

    // Function to make a data request
    function requestData(string memory _dataId) public {
        emit DataRequest(msg.sender, _dataId);
    }

    // Function to update data
    function updateData(string memory _dataId, bytes memory _data) public {
        dataProviders[msg.sender][_dataId] = _data;
        emit DataUpdate(msg.sender, _dataId, _data);
    }

    // Function to get data
    function getData(string memory _dataId) public view returns (bytes memory) {
        return dataProviders[msg.sender][_dataId];
    }
}
