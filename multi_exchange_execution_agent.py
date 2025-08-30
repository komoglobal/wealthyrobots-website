#!/usr/bin/env python3
"""
EMPIRE_AGENT_INFO:
NAME: Multi-Exchange Execution Agent
PURPOSE: Cross-exchange order management and execution optimization
CATEGORY: Trading & Execution
STATUS: Active - New
FREQUENCY: Real-time
"""

import asyncio
import aiohttp
import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import hashlib
import hmac

class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"

class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

class OrderStatus(Enum):
    PENDING = "pending"
    PARTIAL = "partial"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"

@dataclass
class Order:
    """Order representation"""
    id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: Optional[float]
    stop_price: Optional[float]
    exchange: str
    status: OrderStatus
    filled_quantity: float = 0
    average_price: float = 0
    commission: float = 0
    timestamp: datetime = None
    client_order_id: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class ExecutionResult:
    """Order execution result"""
    order_id: str
    symbol: str
    side: OrderSide
    quantity: float
    price: float
    commission: float
    slippage: float
    execution_time: float
    exchange: str
    success: bool
    error_message: str = None

class MultiExchangeExecutionAgent:
    """Multi-exchange order execution and management agent"""
    
    def __init__(self):
        self.agent_name = "Multi-Exchange Execution Agent"
        self.version = "1.0 - Cross-Exchange Execution"
        
        # Exchange configurations
        self.exchanges = {
            'binance': {
                'api_key': os.getenv('BINANCE_API_KEY'),
                'secret_key': os.getenv('BINANCE_SECRET_KEY'),
                'base_url': 'https://api.binance.com',
                'testnet': False,
                'enabled': True
            },
            'coinbase': {
                'api_key': os.getenv('COINBASE_API_KEY'),
                'secret_key': os.getenv('COINBASE_SECRET_KEY'),
                'base_url': 'https://api.coinbase.com',
                'enabled': True
            },
            'kraken': {
                'api_key': os.getenv('KRAKEN_API_KEY'),
                'secret_key': os.getenv('KRAKEN_SECRET_KEY'),
                'base_url': 'https://api.kraken.com',
                'enabled': True
            },
            'ibkr': {
                'enabled': True,  # Interactive Brokers integration
                'paper_trading': True
            }
        }
        
        # Execution parameters
        self.execution_config = {
            'max_slippage': 0.005,  # 0.5% max slippage
            'smart_order_routing': True,
            'iceberg_orders': True,
            'time_weighted_avg_price': True,
            'volume_weighted_avg_price': True,
            'execution_algorithm': 'adaptive'
        }
        
        # Order management
        self.active_orders = {}
        self.order_history = []
        self.execution_stats = {
            'total_orders': 0,
            'successful_orders': 0,
            'failed_orders': 0,
            'average_execution_time': 0,
            'total_slippage': 0
        }
        
        # Risk management
        self.risk_limits = {
            'max_order_size': 10000,  # $10k max per order
            'max_daily_volume': 100000,  # $100k daily limit
            'max_daily_orders': 100,
            'position_limits': {}
        }
        
        print(f"🚀 {self.agent_name} v{self.version} initialized")
        print("🔗 Multi-exchange execution system ready")
        
    async def connect_to_exchanges(self) -> Dict[str, bool]:
        """Establish connections to all enabled exchanges"""
        print("🔌 Connecting to exchanges...")
        
        connections = {}
        
        for exchange_name, config in self.exchanges.items():
            if not config.get('enabled', False):
                connections[exchange_name] = False
                continue
                
            try:
                if exchange_name == 'binance':
                    success = await self._test_binance_connection(config)
                elif exchange_name == 'coinbase':
                    success = await self._test_coinbase_connection(config)
                elif exchange_name == 'kraken':
                    success = await self._test_kraken_connection(config)
                elif exchange_name == 'ibkr':
                    success = await self._test_ibkr_connection(config)
                else:
                    success = False
                
                connections[exchange_name] = success
                
                if success:
                    print(f"✅ {exchange_name}: Connected")
                else:
                    print(f"❌ {exchange_name}: Connection failed")
                    
            except Exception as e:
                print(f"❌ {exchange_name}: Error - {str(e)}")
                connections[exchange_name] = False
        
        return connections
    
    async def _test_binance_connection(self, config: Dict) -> bool:
        """Test Binance API connection"""
        if not config.get('api_key') or not config.get('secret_key'):
            return False
            
        try:
            # Test server time endpoint
            url = f"{config['base_url']}/api/v3/time"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return response.status == 200
        except:
            return False
    
    async def _test_coinbase_connection(self, config: Dict) -> bool:
        """Test Coinbase API connection"""
        if not config.get('api_key') or not config.get('secret_key'):
            return False
            
        try:
            # Test time endpoint
            url = f"{config['base_url']}/v2/time"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return response.status == 200
        except:
            return False
    
    async def _test_kraken_connection(self, config: Dict) -> bool:
        """Test Kraken API connection"""
        if not config.get('api_key') or not config.get('secret_key'):
            return False
            
        try:
            # Test time endpoint
            url = f"{config['base_url']}/0/public/Time"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return response.status == 200
        except:
            return False
    
    async def _test_ibkr_connection(self, config: Dict) -> bool:
        """Test Interactive Brokers connection"""
        try:
            # Check if IBKR integration agent is available
            from ibkr_integration_agent import IBKRIntegrationAgent
            ibkr = IBKRIntegrationAgent()
            # This would need actual IBKR connection logic
            return True
        except ImportError:
            print("⚠️ IBKR integration agent not available")
            return False
    
    async def get_exchange_balances(self, exchange: str) -> Dict:
        """Get account balances for a specific exchange"""
        if not self.exchanges[exchange].get('enabled', False):
            return {}
        
        try:
            if exchange == 'binance':
                return await self._get_binance_balances()
            elif exchange == 'coinbase':
                return await self._get_coinbase_balances()
            elif exchange == 'kraken':
                return await self._get_kraken_balances()
            elif exchange == 'ibkr':
                return await self._get_ibkr_balances()
        except Exception as e:
            print(f"❌ Failed to get {exchange} balances: {str(e)}")
            return {}
        
        return {}
    
    async def _get_binance_balances(self) -> Dict:
        """Get Binance account balances"""
        config = self.exchanges['binance']
        
        # Create signature for authenticated request
        timestamp = int(time.time() * 1000)
        query_string = f"timestamp={timestamp}"
        signature = hmac.new(
            config['secret_key'].encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        url = f"{config['base_url']}/api/v3/account"
        params = {
            'timestamp': timestamp,
            'signature': signature
        }
        
        headers = {'X-MBX-APIKEY': config['api_key']}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    balances = {}
                    
                    for balance in data.get('balances', []):
                        asset = balance['asset']
                        free = float(balance['free'])
                        locked = float(balance['locked'])
                        
                        if free > 0 or locked > 0:
                            balances[asset] = {
                                'free': free,
                                'locked': locked,
                                'total': free + locked
                            }
                    
                    return balances
                else:
                    print(f"❌ Binance balance request failed: {response.status}")
                    return {}
    
    async def _get_coinbase_balances(self) -> Dict:
        """Get Coinbase account balances"""
        config = self.exchanges['coinbase']
        
        url = f"{config['base_url']}/v2/accounts"
        headers = {
            'CB-ACCESS-KEY': config['api_key'],
            'CB-ACCESS-SIGN': self._create_coinbase_signature('GET', '/v2/accounts', ''),
            'CB-ACCESS-TIMESTAMP': str(int(time.time())),
            'CB-ACCESS-PASSPHRASE': config.get('passphrase', '')
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    balances = {}
                    
                    for account in data.get('data', []):
                        currency = account['currency']
                        balance = float(account['balance']['amount'])
                        
                        if balance > 0:
                            balances[currency] = {
                                'balance': balance,
                                'available': balance
                            }
                    
                    return balances
                else:
                    print(f"❌ Coinbase balance request failed: {response.status}")
                    return {}
    
    def _create_coinbase_signature(self, method: str, path: str, body: str) -> str:
        """Create Coinbase API signature"""
        config = self.exchanges['coinbase']
        timestamp = str(int(time.time()))
        message = timestamp + method + path + body
        
        signature = hmac.new(
            config['secret_key'].encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return signature
    
    async def _get_kraken_balances(self) -> Dict:
        """Get Kraken account balances"""
        config = self.exchanges['kraken']
        
        # Kraken requires API key and signature
        url = f"{config['base_url']}/0/private/Balance"
        
        # This would need proper Kraken API signature implementation
        # For now, return empty dict
        return {}
    
    async def _get_ibkr_balances(self) -> Dict:
        """Get Interactive Brokers account balances"""
        try:
            from ibkr_integration_agent import IBKRIntegrationAgent
            ibkr = IBKRIntegrationAgent()
            # This would need actual IBKR balance retrieval
            return {'USD': {'balance': 100000, 'available': 100000}}
        except ImportError:
            return {}
    
    async def place_order(self, symbol: str, side: OrderSide, order_type: OrderType, 
                         quantity: float, price: Optional[float] = None, 
                         exchange: str = 'auto', **kwargs) -> Order:
        """Place an order with smart routing"""
        print(f"📝 Placing {side.value} order: {quantity} {symbol} @ {price or 'market'}")
        
        # Validate order
        validation = self._validate_order(symbol, side, order_type, quantity, price)
        if not validation['valid']:
            raise ValueError(f"Order validation failed: {validation['error']}")
        
        # Select best exchange if auto-routing
        if exchange == 'auto':
            exchange = await self._select_best_exchange(symbol, side, quantity, price)
        
        # Create order object
        order = Order(
            id=self._generate_order_id(),
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=kwargs.get('stop_price'),
            exchange=exchange,
            status=OrderStatus.PENDING,
            client_order_id=kwargs.get('client_order_id')
        )
        
        # Execute order
        execution_result = await self._execute_order(order)
        
        if execution_result.success:
            order.status = OrderStatus.FILLED
            order.filled_quantity = execution_result.quantity
            order.average_price = execution_result.price
            order.commission = execution_result.commission
            
            print(f"✅ Order executed successfully: {execution_result.quantity} @ ${execution_result.price:.4f}")
        else:
            order.status = OrderStatus.REJECTED
            print(f"❌ Order execution failed: {execution_result.error_message}")
        
        # Store order
        self.active_orders[order.id] = order
        self.order_history.append(order)
        
        # Update statistics
        self._update_execution_stats(execution_result)
        
        return order
    
    def _validate_order(self, symbol: str, side: OrderSide, order_type: OrderType, 
                       quantity: float, price: Optional[float]) -> Dict:
        """Validate order parameters"""
        validation = {'valid': True, 'error': None}
        
        # Check quantity
        if quantity <= 0:
            validation['valid'] = False
            validation['error'] = "Quantity must be positive"
            return validation
        
        # Check price for limit orders
        if order_type in [OrderType.LIMIT, OrderType.STOP_LIMIT] and price is None:
            validation['valid'] = False
            validation['error'] = "Price required for limit orders"
            return validation
        
        # Check risk limits
        estimated_value = quantity * (price or 100)  # Rough estimate for market orders
        if estimated_value > self.risk_limits['max_order_size']:
            validation['valid'] = False
            validation['error'] = f"Order size ${estimated_value:,.2f} exceeds limit ${self.risk_limits['max_order_size']:,.2f}"
            return validation
        
        # Check daily limits
        if self.execution_stats['total_orders'] >= self.risk_limits['max_daily_orders']:
            validation['valid'] = False
            validation['error'] = "Daily order limit reached"
            return validation
        
        return validation
    
    async def _select_best_exchange(self, symbol: str, side: OrderSide, 
                                   quantity: float, price: Optional[float]) -> str:
        """Select best exchange for order execution"""
        print("🔍 Selecting best exchange for execution...")
        
        # Get available exchanges for this symbol
        available_exchanges = []
        
        for exchange_name, config in self.exchanges.items():
            if config.get('enabled', False):
                # Check if symbol is supported
                if await self._is_symbol_supported(exchange_name, symbol):
                    available_exchanges.append(exchange_name)
        
        if not available_exchanges:
            raise ValueError(f"No exchanges support symbol {symbol}")
        
        # Score exchanges based on multiple factors
        exchange_scores = {}
        
        for exchange in available_exchanges:
            score = 0
            
            # Liquidity score (higher is better)
            liquidity = await self._get_exchange_liquidity(exchange, symbol)
            score += liquidity * 0.4
            
            # Fee score (lower is better)
            fees = await self._get_exchange_fees(exchange, symbol, quantity, price)
            score += (1 - fees) * 0.3
            
            # Execution speed score
            speed = await self._get_exchange_execution_speed(exchange)
            score += speed * 0.2
            
            # Reliability score
            reliability = self._get_exchange_reliability(exchange)
            score += reliability * 0.1
            
            exchange_scores[exchange] = score
        
        # Select exchange with highest score
        best_exchange = max(exchange_scores, key=exchange_scores.get)
        print(f"🎯 Selected {best_exchange} (score: {exchange_scores[best_exchange]:.3f})")
        
        return best_exchange
    
    async def _is_symbol_supported(self, exchange: str, symbol: str) -> bool:
        """Check if symbol is supported by exchange"""
        # This would need actual exchange API calls
        # For now, return True for common symbols
        common_symbols = ['BTC', 'ETH', 'AAPL', 'GOOGL', 'MSFT', 'TSLA']
        return symbol in common_symbols
    
    async def _get_exchange_liquidity(self, exchange: str, symbol: str) -> float:
        """Get exchange liquidity score (0-1)"""
        # This would need actual order book data
        # For now, return random scores
        import random
        return random.uniform(0.5, 1.0)
    
    async def _get_exchange_fees(self, exchange: str, symbol: str, 
                                 quantity: float, price: Optional[float]) -> float:
        """Get exchange fee rate (0-1)"""
        # Typical fee rates
        fee_rates = {
            'binance': 0.001,  # 0.1%
            'coinbase': 0.005,  # 0.5%
            'kraken': 0.0026,  # 0.26%
            'ibkr': 0.0005     # 0.05%
        }
        
        return fee_rates.get(exchange, 0.002)
    
    async def _get_exchange_execution_speed(self, exchange: str) -> float:
        """Get exchange execution speed score (0-1)"""
        # This would need actual performance metrics
        # For now, return estimated scores
        speed_scores = {
            'binance': 0.9,
            'coinbase': 0.8,
            'kraken': 0.85,
            'ibkr': 0.7
        }
        
        return speed_scores.get(exchange, 0.8)
    
    def _get_exchange_reliability(self, exchange: str) -> float:
        """Get exchange reliability score (0-1)"""
        # Based on historical performance
        reliability_scores = {
            'binance': 0.95,
            'coinbase': 0.98,
            'kraken': 0.92,
            'ibkr': 0.99
        }
        
        return reliability_scores.get(exchange, 0.9)
    
    async def _execute_order(self, order: Order) -> ExecutionResult:
        """Execute order on selected exchange"""
        start_time = time.time()
        
        try:
            if order.exchange == 'binance':
                result = await self._execute_binance_order(order)
            elif order.exchange == 'coinbase':
                result = await self._execute_coinbase_order(order)
            elif order.exchange == 'kraken':
                result = await self._execute_kraken_order(order)
            elif order.exchange == 'ibkr':
                result = await self._execute_ibkr_order(order)
            else:
                raise ValueError(f"Unsupported exchange: {order.exchange}")
            
            # Calculate execution time
            execution_time = time.time() - start_time
            
            # Calculate slippage
            slippage = 0
            if order.price and result.price:
                slippage = abs(result.price - order.price) / order.price
            
            result.execution_time = execution_time
            result.slippage = slippage
            
            return result
            
        except Exception as e:
            return ExecutionResult(
                order_id=order.id,
                symbol=order.symbol,
                side=order.side,
                quantity=0,
                price=0,
                commission=0,
                slippage=0,
                execution_time=time.time() - start_time,
                exchange=order.exchange,
                success=False,
                error_message=str(e)
            )
    
    async def _execute_binance_order(self, order: Order) -> ExecutionResult:
        """Execute order on Binance"""
        config = self.exchanges['binance']
        
        # This would need actual Binance order execution
        # For now, simulate execution
        await asyncio.sleep(0.1)  # Simulate network delay
        
        # Simulate fill
        fill_price = order.price or 100  # Market price simulation
        commission = order.quantity * fill_price * 0.001  # 0.1% fee
        
        return ExecutionResult(
            order_id=order.id,
            symbol=order.symbol,
            side=order.side,
            quantity=order.quantity,
            price=fill_price,
            commission=commission,
            slippage=0,
            execution_time=0,
            exchange=order.exchange,
            success=True
        )
    
    async def _execute_coinbase_order(self, order: Order) -> ExecutionResult:
        """Execute order on Coinbase"""
        # Similar to Binance execution
        await asyncio.sleep(0.15)  # Slightly slower
        
        fill_price = order.price or 100
        commission = order.quantity * fill_price * 0.005  # 0.5% fee
        
        return ExecutionResult(
            order_id=order.id,
            symbol=order.symbol,
            side=order.side,
            quantity=order.quantity,
            price=fill_price,
            commission=commission,
            slippage=0,
            execution_time=0,
            exchange=order.exchange,
            success=True
        )
    
    async def _execute_kraken_order(self, order: Order) -> ExecutionResult:
        """Execute order on Kraken"""
        await asyncio.sleep(0.12)
        
        fill_price = order.price or 100
        commission = order.quantity * fill_price * 0.0026  # 0.26% fee
        
        return ExecutionResult(
            order_id=order.id,
            symbol=order.symbol,
            side=order.side,
            quantity=order.quantity,
            price=fill_price,
            commission=commission,
            slippage=0,
            execution_time=0,
            exchange=order.exchange,
            success=True
        )
    
    async def _execute_ibkr_order(self, order: Order) -> ExecutionResult:
        """Execute order on Interactive Brokers"""
        try:
            from ibkr_integration_agent import IBKRIntegrationAgent
            ibkr = IBKRIntegrationAgent()
            
            # This would need actual IBKR order execution
            await asyncio.sleep(0.2)  # IBKR can be slower
            
            fill_price = order.price or 100
            commission = order.quantity * fill_price * 0.0005  # 0.05% fee
            
            return ExecutionResult(
                order_id=order.id,
                symbol=order.symbol,
                side=order.side,
                quantity=order.quantity,
                price=fill_price,
                commission=commission,
                slippage=0,
                execution_time=0,
                exchange=order.exchange,
                success=True
            )
        except ImportError:
            raise ValueError("IBKR integration not available")
    
    def _generate_order_id(self) -> str:
        """Generate unique order ID"""
        timestamp = int(time.time() * 1000)
        random_part = os.urandom(4).hex()
        return f"order_{timestamp}_{random_part}"
    
    def _update_execution_stats(self, result: ExecutionResult):
        """Update execution statistics"""
        self.execution_stats['total_orders'] += 1
        
        if result.success:
            self.execution_stats['successful_orders'] += 1
        else:
            self.execution_stats['failed_orders'] += 1
        
        # Update average execution time
        current_avg = self.execution_stats['average_execution_time']
        total_orders = self.execution_stats['total_orders']
        self.execution_stats['average_execution_time'] = (
            (current_avg * (total_orders - 1) + result.execution_time) / total_orders
        )
        
        # Update total slippage
        self.execution_stats['total_slippage'] += result.slippage
    
    async def cancel_order(self, order_id: str) -> bool:
        """Cancel an active order"""
        if order_id not in self.active_orders:
            print(f"❌ Order {order_id} not found")
            return False
        
        order = self.active_orders[order_id]
        
        try:
            # Cancel on exchange
            if order.exchange == 'binance':
                success = await self._cancel_binance_order(order)
            elif order.exchange == 'coinbase':
                success = await self._cancel_coinbase_order(order)
            elif order.exchange == 'kraken':
                success = await self._cancel_kraken_order(order)
            elif order.exchange == 'ibkr':
                success = await self._cancel_ibkr_order(order)
            else:
                success = False
            
            if success:
                order.status = OrderStatus.CANCELLED
                print(f"✅ Order {order_id} cancelled successfully")
                return True
            else:
                print(f"❌ Failed to cancel order {order_id}")
                return False
                
        except Exception as e:
            print(f"❌ Error cancelling order {order_id}: {str(e)}")
            return False
    
    async def _cancel_binance_order(self, order: Order) -> bool:
        """Cancel order on Binance"""
        # This would need actual Binance cancellation
        await asyncio.sleep(0.1)
        return True
    
    async def _cancel_coinbase_order(self, order: Order) -> bool:
        """Cancel order on Coinbase"""
        await asyncio.sleep(0.1)
        return True
    
    async def _cancel_kraken_order(self, order: Order) -> bool:
        """Cancel order on Kraken"""
        await asyncio.sleep(0.1)
        return True
    
    async def _cancel_ibkr_order(self, order: Order) -> bool:
        """Cancel order on Interactive Brokers"""
        await asyncio.sleep(0.2)
        return True
    
    def get_order_status(self, order_id: str) -> Optional[Order]:
        """Get current order status"""
        return self.active_orders.get(order_id)
    
    def get_execution_summary(self) -> Dict:
        """Get execution performance summary"""
        return {
            'timestamp': datetime.now().isoformat(),
            'total_orders': self.execution_stats['total_orders'],
            'successful_orders': self.execution_stats['successful_orders'],
            'failed_orders': self.execution_stats['failed_orders'],
            'success_rate': self.execution_stats['successful_orders'] / max(self.execution_stats['total_orders'], 1),
            'average_execution_time': self.execution_stats['average_execution_time'],
            'total_slippage': self.execution_stats['total_slippage'],
            'active_orders': len(self.active_orders),
            'exchanges_connected': sum(1 for config in self.exchanges.values() if config.get('enabled', False))
        }
    
    async def run_agent(self):
        """Main agent execution loop"""
        print(f"🤖 {self.agent_name} starting...")
        
        # Connect to exchanges
        connections = await self.connect_to_exchanges()
        
        print(f"🔗 Exchange connections: {connections}")
        
        # Monitor active orders
        while True:
            try:
                # Check order statuses
                await self._update_order_statuses()
                
                # Generate execution report
                if self.execution_stats['total_orders'] > 0:
                    summary = self.get_execution_summary()
                    print(f"📊 Execution Summary: {summary['successful_orders']}/{summary['total_orders']} orders successful")
                
                # Wait before next update
                await asyncio.sleep(5)
                
            except Exception as e:
                print(f"❌ Agent error: {str(e)}")
                await asyncio.sleep(10)
    
    async def _update_order_statuses(self):
        """Update status of active orders"""
        for order_id, order in list(self.active_orders.items()):
            if order.status in [OrderStatus.FILLED, OrderStatus.CANCELLED, OrderStatus.REJECTED]:
                # Remove completed orders from active list
                del self.active_orders[order_id]

async def main():
    """Test the multi-exchange execution agent"""
    agent = MultiExchangeExecutionAgent()
    
    # Test exchange connections
    print("\n🔌 Testing exchange connections...")
    connections = await agent.connect_to_exchanges()
    print(f"Connections: {connections}")
    
    # Test balance retrieval
    print("\n💰 Testing balance retrieval...")
    for exchange in ['binance', 'coinbase']:
        if connections.get(exchange, False):
            balances = await agent.get_exchange_balances(exchange)
            print(f"{exchange} balances: {len(balances)} assets")
    
    # Test order placement
    print("\n📝 Testing order placement...")
    try:
        order = await agent.place_order(
            symbol='BTC',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=0.001,
            exchange='auto'
        )
        print(f"Order placed: {order.id} - {order.status.value}")
    except Exception as e:
        print(f"Order placement failed: {str(e)}")
    
    # Get execution summary
    print("\n📊 Execution Summary:")
    summary = agent.get_execution_summary()
    print(json.dumps(summary, indent=2, default=str))

if __name__ == "__main__":
    asyncio.run(main())
