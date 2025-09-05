import React, { useState } from 'react';
import { TrendingUp, TrendingDown, Activity, DollarSign, BarChart3 } from 'lucide-react';

const Trading = () => {
  const [activeTab, setActiveTab] = useState('buy');
  const [selectedCrypto, setSelectedCrypto] = useState('BTC');
  const [orderType, setOrderType] = useState('market');

  const cryptoData = [
    {
      symbol: 'BTC',
      name: 'بیت‌کوین',
      price: '2,650,000,000',
      change: '+2.5%',
      changeType: 'increase',
      volume: '124.5M',
      high: '2,680,000,000',
      low: '2,590,000,000'
    },
    {
      symbol: 'ETH',
      name: 'اتریوم',
      price: '165,000,000',
      change: '-1.2%',
      changeType: 'decrease',
      volume: '89.2M',
      high: '168,000,000',
      low: '162,000,000'
    },
    {
      symbol: 'ADA',
      name: 'کاردانو',
      price: '18,500',
      change: '+5.8%',
      changeType: 'increase',
      volume: '45.7M',
      high: '19,200',
      low: '17,800'
    },
    {
      symbol: 'SOL',
      name: 'سولانا',
      price: '4,200,000',
      change: '+8.2%',
      changeType: 'increase',
      volume: '67.3M',
      high: '4,350,000',
      low: '3,980,000'
    }
  ];

  const orderBook = [
    { price: '2,652,000,000', amount: '0.0245', type: 'sell' },
    { price: '2,651,000,000', amount: '0.0180', type: 'sell' },
    { price: '2,650,000,000', amount: '0.0320', type: 'sell' },
    { price: '2,649,000,000', amount: '0.0156', type: 'buy' },
    { price: '2,648,000,000', amount: '0.0290', type: 'buy' },
    { price: '2,647,000,000', amount: '0.0220', type: 'buy' },
  ];

  const recentTrades = [
    { price: '2,650,000,000', amount: '0.0120', time: '14:25:30', type: 'buy' },
    { price: '2,649,000,000', amount: '0.0086', time: '14:25:28', type: 'sell' },
    { price: '2,651,000,000', amount: '0.0234', time: '14:25:25', type: 'buy' },
    { price: '2,648,000,000', amount: '0.0145', time: '14:25:22', type: 'sell' },
    { price: '2,650,000,000', amount: '0.0078', time: '14:25:20', type: 'buy' },
  ];

  const selectedCryptoData = cryptoData.find(crypto => crypto.symbol === selectedCrypto);

  return (
    <div className="min-h-screen bg-dark-900 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">پلتفرم معاملات</h1>
          <p className="text-gray-400">خرید و فروش ارزهای دیجیتال</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Crypto List */}
          <div className="lg:col-span-1">
            <div className="bg-dark-800 rounded-lg p-6">
              <h2 className="text-lg font-bold text-white mb-4">بازار ارزها</h2>
              <div className="space-y-2">
                {cryptoData.map((crypto) => (
                  <div
                    key={crypto.symbol}
                    className={`p-3 rounded-lg cursor-pointer transition-colors ${
                      selectedCrypto === crypto.symbol 
                        ? 'bg-primary-600 text-white' 
                        : 'bg-dark-700 hover:bg-dark-600 text-gray-300'
                    }`}
                    onClick={() => setSelectedCrypto(crypto.symbol)}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="font-medium">{crypto.symbol}</div>
                        <div className="text-sm opacity-75">{crypto.name}</div>
                      </div>
                      <div className="text-right">
                        <div className="text-sm font-medium">{crypto.price}</div>
                        <div className={`text-xs ${
                          crypto.changeType === 'increase' ? 'text-green-400' : 'text-red-400'
                        }`}>
                          {crypto.change}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Chart Area */}
          <div className="lg:col-span-2">
            <div className="bg-dark-800 rounded-lg p-6 mb-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-bold text-white">
                  {selectedCryptoData?.name} ({selectedCryptoData?.symbol})
                </h2>
                <div className="flex items-center space-x-4 space-x-reverse">
                  <span className="text-2xl font-bold text-white">
                    {selectedCryptoData?.price} تومان
                  </span>
                  <span className={`text-sm font-medium ${
                    selectedCryptoData?.changeType === 'increase' ? 'text-green-400' : 'text-red-400'
                  }`}>
                    {selectedCryptoData?.change}
                  </span>
                </div>
              </div>
              
              {/* Mock Chart */}
              <div className="h-64 bg-dark-700 rounded-lg flex items-center justify-center">
                <div className="text-center">
                  <BarChart3 className="h-16 w-16 text-gray-500 mx-auto mb-4" />
                  <p className="text-gray-400">نمودار قیمت {selectedCryptoData?.name}</p>
                </div>
              </div>

              {/* Market Stats */}
              <div className="grid grid-cols-3 gap-4 mt-4">
                <div className="text-center">
                  <p className="text-sm text-gray-400">حجم 24 ساعته</p>
                  <p className="text-lg font-medium text-white">{selectedCryptoData?.volume}</p>
                </div>
                <div className="text-center">
                  <p className="text-sm text-gray-400">بالاترین قیمت</p>
                  <p className="text-lg font-medium text-white">{selectedCryptoData?.high}</p>
                </div>
                <div className="text-center">
                  <p className="text-sm text-gray-400">پایین‌ترین قیمت</p>
                  <p className="text-lg font-medium text-white">{selectedCryptoData?.low}</p>
                </div>
              </div>
            </div>

            {/* Order Book & Recent Trades */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-dark-800 rounded-lg p-6">
                <h3 className="text-lg font-bold text-white mb-4">دفتر سفارشات</h3>
                <div className="space-y-2">
                  <div className="grid grid-cols-2 gap-4 text-sm text-gray-400 border-b border-dark-600 pb-2">
                    <span>قیمت (تومان)</span>
                    <span>مقدار</span>
                  </div>
                  {orderBook.map((order, index) => (
                    <div 
                      key={index} 
                      className={`grid grid-cols-2 gap-4 text-sm py-1 ${
                        order.type === 'sell' ? 'text-red-400' : 'text-green-400'
                      }`}
                    >
                      <span>{order.price}</span>
                      <span>{order.amount}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-dark-800 rounded-lg p-6">
                <h3 className="text-lg font-bold text-white mb-4">معاملات اخیر</h3>
                <div className="space-y-2">
                  <div className="grid grid-cols-3 gap-4 text-sm text-gray-400 border-b border-dark-600 pb-2">
                    <span>قیمت</span>
                    <span>مقدار</span>
                    <span>زمان</span>
                  </div>
                  {recentTrades.map((trade, index) => (
                    <div 
                      key={index} 
                      className={`grid grid-cols-3 gap-4 text-sm py-1 ${
                        trade.type === 'buy' ? 'text-green-400' : 'text-red-400'
                      }`}
                    >
                      <span>{trade.price}</span>
                      <span>{trade.amount}</span>
                      <span className="text-gray-400">{trade.time}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Trading Panel */}
          <div className="lg:col-span-1">
            <div className="bg-dark-800 rounded-lg p-6">
              <div className="flex rounded-lg bg-dark-700 p-1 mb-6">
                <button
                  onClick={() => setActiveTab('buy')}
                  className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                    activeTab === 'buy' 
                      ? 'bg-green-600 text-white' 
                      : 'text-gray-400 hover:text-white'
                  }`}
                >
                  خرید
                </button>
                <button
                  onClick={() => setActiveTab('sell')}
                  className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                    activeTab === 'sell' 
                      ? 'bg-red-600 text-white' 
                      : 'text-gray-400 hover:text-white'
                  }`}
                >
                  فروش
                </button>
              </div>

              {/* Order Type */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  نوع سفارش
                </label>
                <select 
                  value={orderType}
                  onChange={(e) => setOrderType(e.target.value)}
                  className="w-full bg-dark-700 border border-dark-600 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="market">بازار</option>
                  <option value="limit">محدود</option>
                  <option value="stop">استاپ</option>
                </select>
              </div>

              {/* Price Input */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  قیمت (تومان)
                </label>
                <input
                  type="text"
                  value={selectedCryptoData?.price}
                  disabled={orderType === 'market'}
                  className="w-full bg-dark-700 border border-dark-600 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:opacity-50"
                />
              </div>

              {/* Amount Input */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  مقدار ({selectedCrypto})
                </label>
                <input
                  type="number"
                  step="0.00001"
                  placeholder="0.00000"
                  className="w-full bg-dark-700 border border-dark-600 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>

              {/* Total */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  کل (تومان)
                </label>
                <input
                  type="text"
                  placeholder="0"
                  className="w-full bg-dark-700 border border-dark-600 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>

              {/* Percentage Buttons */}
              <div className="grid grid-cols-4 gap-2 mb-6">
                {['25%', '50%', '75%', '100%'].map((percent) => (
                  <button
                    key={percent}
                    className="py-2 px-3 text-sm bg-dark-700 hover:bg-dark-600 text-gray-300 rounded-md transition-colors"
                  >
                    {percent}
                  </button>
                ))}
              </div>

              {/* Submit Button */}
              <button
                className={`w-full py-3 px-4 rounded-md font-medium transition-colors ${
                  activeTab === 'buy'
                    ? 'bg-green-600 hover:bg-green-700 text-white'
                    : 'bg-red-600 hover:bg-red-700 text-white'
                }`}
              >
                {activeTab === 'buy' ? 'خرید' : 'فروش'} {selectedCrypto}
              </button>

              {/* Balance Info */}
              <div className="mt-6 pt-6 border-t border-dark-600">
                <h4 className="text-sm font-medium text-gray-300 mb-3">موجودی</h4>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">تومان</span>
                    <span className="text-white">125,000,000</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">{selectedCrypto}</span>
                    <span className="text-white">0.00456</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Trading;