"""
Market data collector service
Collects cryptocurrency market data from multiple exchanges using ccxt
"""
import ccxt
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MarketCollector:
    """Collects market data from multiple exchanges"""
    
    def __init__(self, exchanges: List[str]):
        """
        Initialize market collector
        
        Args:
            exchanges: List of exchange names (e.g., ['binance', 'okx', 'bybit'])
        """
        self.exchanges = {}
        self.exchange_names = exchanges
        
        # Initialize exchange instances
        for exchange_name in exchanges:
            try:
                exchange_class = getattr(ccxt, exchange_name)
                self.exchanges[exchange_name] = exchange_class({
                    'enableRateLimit': True,
                    'options': {
                        'defaultType': 'spot'
                    }
                })
                logger.info(f"Initialized exchange: {exchange_name}")
            except Exception as e:
                logger.error(f"Failed to initialize {exchange_name}: {e}")
    
    async def get_ticker(self, exchange_name: str, symbol: str) -> Optional[Dict]:
        """
        Get ticker data for a symbol from an exchange
        
        Args:
            exchange_name: Name of the exchange
            symbol: Trading pair symbol (e.g., 'BTC/USDT')
        
        Returns:
            Dict with ticker data or None if error
        """
        if exchange_name not in self.exchanges:
            return None
        
        exchange = self.exchanges[exchange_name]
        
        try:
            ticker = exchange.fetch_ticker(symbol)
            return {
                'symbol': symbol,
                'price': ticker.get('last', 0),
                'volume_24h': ticker.get('quoteVolume', 0),
                'change_24h': ticker.get('percentage', 0),
                'high_24h': ticker.get('high', 0),
                'low_24h': ticker.get('low', 0),
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error fetching {symbol} from {exchange_name}: {e}")
            return None
    
    async def get_top_pairs(self, exchange_name: str, limit: int = 50) -> List[Dict]:
        """
        Get top trading pairs by volume from an exchange
        
        Args:
            exchange_name: Name of the exchange
            limit: Number of top pairs to return
        
        Returns:
            List of ticker data dictionaries
        """
        if exchange_name not in self.exchanges:
            return []
        
        exchange = self.exchanges[exchange_name]
        results = []
        
        try:
            # Get all tickers
            tickers = exchange.fetch_tickers()
            
            # Filter USDT pairs and sort by volume
            usdt_pairs = [
                ticker for symbol, ticker in tickers.items()
                if '/USDT' in symbol and ticker.get('quoteVolume', 0) > 0
            ]
            
            # Sort by volume and take top N
            usdt_pairs.sort(key=lambda x: x.get('quoteVolume', 0), reverse=True)
            top_pairs = usdt_pairs[:limit]
            
            for ticker in top_pairs:
                results.append({
                    'symbol': ticker['symbol'],
                    'price': ticker.get('last', 0),
                    'volume_24h': ticker.get('quoteVolume', 0),
                    'change_24h': ticker.get('percentage', 0),
                    'high_24h': ticker.get('high', 0),
                    'low_24h': ticker.get('low', 0),
                    'timestamp': datetime.utcnow().isoformat()
                })
        
        except Exception as e:
            logger.error(f"Error fetching top pairs from {exchange_name}: {e}")
        
        return results
    
    async def collect_all_exchanges(self, symbols: Optional[List[str]] = None, 
                                   top_pairs_limit: int = 50) -> Dict[str, List[Dict]]:
        """
        Collect market data from all configured exchanges
        
        Args:
            symbols: Optional list of specific symbols to fetch
            top_pairs_limit: Number of top pairs to fetch if symbols not specified
        
        Returns:
            Dict mapping exchange names to lists of ticker data
        """
        results = {}
        
        # Create tasks with metadata
        tasks_with_info = []
        for exchange_name in self.exchange_names:
            if exchange_name in self.exchanges:
                if symbols:
                    # Fetch specific symbols
                    for symbol in symbols:
                        task = self.get_ticker(exchange_name, symbol)
                        tasks_with_info.append((exchange_name, symbol, task, True))
                else:
                    # Fetch top pairs
                    task = self.get_top_pairs(exchange_name, top_pairs_limit)
                    tasks_with_info.append((exchange_name, None, task, False))
        
        # Execute all tasks concurrently
        task_results = await asyncio.gather(
            *[task for _, _, task, _ in tasks_with_info],
            return_exceptions=True
        )
        
        # Process results
        for i, (exchange_name, symbol, _, is_ticker) in enumerate(tasks_with_info):
            result = task_results[i]
            
            if isinstance(result, Exception):
                logger.error(f"Error in collection task for {exchange_name}: {result}")
                continue
            
            if exchange_name not in results:
                results[exchange_name] = []
            
            if is_ticker:
                # Single ticker result
                if result:
                    results[exchange_name].append(result)
            else:
                # List of tickers
                if isinstance(result, list):
                    results[exchange_name].extend(result)
        
        return results
    
    async def get_market_pulse(self, top_pairs_limit: int = 50) -> List[Dict]:
        """
        Get aggregated market pulse data across all exchanges
        
        Args:
            top_pairs_limit: Number of top pairs per exchange
        
        Returns:
            List of aggregated market data
        """
        all_data = await self.collect_all_exchanges(top_pairs_limit=top_pairs_limit)
        
        # Aggregate data by symbol across exchanges
        symbol_map = {}
        
        for exchange_name, tickers in all_data.items():
            for ticker in tickers:
                symbol = ticker['symbol']
                if symbol not in symbol_map:
                    symbol_map[symbol] = {
                        'symbol': symbol,
                        'exchanges': [],
                        'avg_price': 0,
                        'total_volume_24h': 0,
                        'avg_change_24h': 0,
                        'max_change_24h': 0
                    }
                
                symbol_map[symbol]['exchanges'].append({
                    'exchange': exchange_name,
                    'price': ticker['price'],
                    'volume_24h': ticker['volume_24h'],
                    'change_24h': ticker['change_24h']
                })
                
                symbol_map[symbol]['total_volume_24h'] += ticker['volume_24h']
        
        # Calculate averages
        for symbol, data in symbol_map.items():
            if data['exchanges']:
                prices = [e['price'] for e in data['exchanges']]
                changes = [e['change_24h'] for e in data['exchanges']]
                
                data['avg_price'] = sum(prices) / len(prices)
                data['avg_change_24h'] = sum(changes) / len(changes)
                data['max_change_24h'] = max(changes)
        
        # Sort by total volume
        pulse_list = sorted(symbol_map.values(), 
                          key=lambda x: x['total_volume_24h'], 
                          reverse=True)
        
        return pulse_list[:top_pairs_limit]

