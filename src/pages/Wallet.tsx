import React, { useState } from 'react';
import { Wallet, CreditCard, ArrowUpRight, ArrowDownRight, History, Eye, EyeOff } from 'lucide-react';

const WalletPage = () => {
  const [showBalance, setShowBalance] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  const balances = [
    {
      symbol: 'BTC',
      name: 'بیت‌کوین',
      amount: '0.00456',
      value: '120,840,000',
      change: '+2.5%',
      changeType: 'increase'
    },
    {
      symbol: 'ETH',
      name: 'اتریوم',
      amount: '0.123',
      value: '20,295,000',
      change: '-1.2%',
      changeType: 'decrease'
    },
    {
      symbol: 'USDT',
      name: 'تتر',
      amount: '1,250',
      value: '52,500,000',
      change: '+0.1%',
      changeType: 'increase'
    },
    {
      symbol: 'ADA',
      name: 'کاردانو',
      amount: '850',
      value: '15,725,000',
      change: '+5.8%',
      changeType: 'increase'
    },
    {
      symbol: 'IRR',
      name: 'تومان',
      amount: '125,000,000',
      value: '125,000,000',
      change: '0%',
      changeType: 'neutral'
    }
  ];

  const transactions = [
    {
      type: 'واریز',
      crypto: 'بیت‌کوین',
      amount: '+0.0012',
      value: '+3,180,000',
      date: '۱۴۰۲/۰۹/۱۵',
      time: '14:25',
      status: 'تأیید شده',
      txHash: 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh'
    },
    {
      type: 'برداشت',
      crypto: 'اتریوم',
      amount: '-0.05',
      value: '-8,250,000',
      date: '۱۴۰۲/۰۹/۱۴',
      time: '16:30',
      status: 'تأیید شده',
      txHash: '0x742d35Cc6634C0532925a3b8D2aE16eC88D6399b'
    },
    {
      type: 'واریز',
      crypto: 'تومان',
      amount: '+50,000,000',
      value: '+50,000,000',
      date: '۱۴۰۲/۰۹/۱۳',
      time: '10:15',
      status: 'تأیید شده',
      txHash: '1234567890123456'
    },
    {
      type: 'برداشت',
      crypto: 'کاردانو',
      amount: '-100',
      value: '-1,850,000',
      date: '۱۴۰۲/۰۹/۱۲',
      time: '12:45',
      status: 'در حال پردازش',
      txHash: 'addr1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh'
    },
    {
      type: 'واریز',
      crypto: 'سولانا',
      amount: '+1.5',
      value: '+6,300,000',
      date: '۱۴۰۲/۰۹/۱۱',
      time: '09:20',
      status: 'تأیید شده',
      txHash: '3K2b8FHdKkdPwdJoSz6zYqNYGFNh7vHbA5mC8nN4DjKL'
    }
  ];

  const totalBalance = balances.reduce((sum, balance) => sum + parseFloat(balance.value.replace(/,/g, '')), 0);

  return (
    <div className="min-h-screen bg-dark-900 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">کیف پول</h1>
          <p className="text-gray-400">مدیریت موجودی و تراکنش‌های شما</p>
        </div>

        {/* Total Balance Card */}
        <div className="bg-gradient-to-r from-primary-600 to-secondary-600 rounded-lg p-8 mb-8">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-primary-100 text-sm mb-2">کل موجودی</p>
              <div className="flex items-center space-x-4 space-x-reverse">
                <span className="text-4xl font-bold text-white">
                  {showBalance ? `${totalBalance.toLocaleString()} تومان` : '••••••••'}
                </span>
                <button
                  onClick={() => setShowBalance(!showBalance)}
                  className="text-primary-100 hover:text-white transition-colors"
                >
                  {showBalance ? <EyeOff className="h-6 w-6" /> : <Eye className="h-6 w-6" />}
                </button>
              </div>
            </div>
            <div className="text-right">
              <p className="text-primary-100 text-sm mb-2">سود کل</p>
              <p className="text-2xl font-bold text-white">+12.5%</p>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <button className="bg-green-600 hover:bg-green-700 text-white p-6 rounded-lg font-medium transition-colors flex items-center justify-center space-x-2 space-x-reverse">
            <ArrowDownRight className="h-5 w-5" />
            <span>واریز</span>
          </button>
          <button className="bg-red-600 hover:bg-red-700 text-white p-6 rounded-lg font-medium transition-colors flex items-center justify-center space-x-2 space-x-reverse">
            <ArrowUpRight className="h-5 w-5" />
            <span>برداشت</span>
          </button>
          <button className="bg-primary-600 hover:bg-primary-700 text-white p-6 rounded-lg font-medium transition-colors flex items-center justify-center space-x-2 space-x-reverse">
            <CreditCard className="h-5 w-5" />
            <span>تبدیل</span>
          </button>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-dark-700 mb-8">
          <button
            onClick={() => setActiveTab('overview')}
            className={`py-4 px-6 font-medium transition-colors ${
              activeTab === 'overview'
                ? 'border-b-2 border-primary-500 text-primary-500'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            نمای کلی
          </button>
          <button
            onClick={() => setActiveTab('transactions')}
            className={`py-4 px-6 font-medium transition-colors ${
              activeTab === 'transactions'
                ? 'border-b-2 border-primary-500 text-primary-500'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            تاریخچه تراکنش‌ها
          </button>
        </div>

        {/* Content */}
        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Assets */}
            <div className="bg-dark-800 rounded-lg p-6">
              <h2 className="text-xl font-bold text-white mb-6">دارایی‌ها</h2>
              <div className="space-y-4">
                {balances.map((balance, index) => (
                  <div key={index} className="flex items-center justify-between p-4 bg-dark-700 rounded-lg hover:bg-dark-600 transition-colors">
                    <div className="flex items-center">
                      <div className="w-12 h-12 bg-primary-600 rounded-full flex items-center justify-center ml-4">
                        <span className="text-white font-bold">{balance.symbol}</span>
                      </div>
                      <div>
                        <h3 className="font-medium text-white">{balance.name}</h3>
                        <p className="text-sm text-gray-400">{balance.amount} {balance.symbol}</p>
                      </div>
                    </div>
                    <div className="text-left">
                      <p className="font-medium text-white">
                        {showBalance ? `${balance.value} تومان` : '••••••'}
                      </p>
                      <span className={`text-sm font-medium ${
                        balance.changeType === 'increase' ? 'text-green-400' :
                        balance.changeType === 'decrease' ? 'text-red-400' : 'text-gray-400'
                      }`}>
                        {balance.change}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Recent Activity */}
            <div className="bg-dark-800 rounded-lg p-6">
              <h2 className="text-xl font-bold text-white mb-6">فعالیت اخیر</h2>
              <div className="space-y-4">
                {transactions.slice(0, 5).map((transaction, index) => (
                  <div key={index} className="flex items-center justify-between p-4 bg-dark-700 rounded-lg">
                    <div className="flex items-center">
                      <div className={`w-10 h-10 rounded-full flex items-center justify-center ml-4 ${
                        transaction.type === 'واریز' ? 'bg-green-600' : 'bg-red-600'
                      }`}>
                        {transaction.type === 'واریز' ? 
                          <ArrowDownRight className="h-5 w-5 text-white" /> : 
                          <ArrowUpRight className="h-5 w-5 text-white" />
                        }
                      </div>
                      <div>
                        <h3 className="font-medium text-white">{transaction.type} {transaction.crypto}</h3>
                        <p className="text-sm text-gray-400">{transaction.date} - {transaction.time}</p>
                      </div>
                    </div>
                    <div className="text-left">
                      <p className={`font-medium ${
                        transaction.type === 'واریز' ? 'text-green-400' : 'text-red-400'
                      }`}>
                        {transaction.amount}
                      </p>
                      <p className="text-sm text-gray-400">{transaction.value} تومان</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'transactions' && (
          <div className="bg-dark-800 rounded-lg p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-white">تاریخچه تراکنش‌ها</h2>
              <select className="bg-dark-700 border border-dark-600 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500">
                <option>همه تراکنش‌ها</option>
                <option>واریز</option>
                <option>برداشت</option>
              </select>
            </div>
            
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-dark-600">
                    <th className="text-right py-3 px-4 text-sm font-medium text-gray-400">نوع</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-gray-400">ارز</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-gray-400">مقدار</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-gray-400">ارزش</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-gray-400">تاریخ</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-gray-400">وضعیت</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-gray-400">شناسه</th>
                  </tr>
                </thead>
                <tbody>
                  {transactions.map((transaction, index) => (
                    <tr key={index} className="border-b border-dark-700 hover:bg-dark-700 transition-colors">
                      <td className="py-4 px-4">
                        <div className="flex items-center">
                          <div className={`w-8 h-8 rounded-full flex items-center justify-center ml-2 ${
                            transaction.type === 'واریز' ? 'bg-green-600' : 'bg-red-600'
                          }`}>
                            {transaction.type === 'واریز' ? 
                              <ArrowDownRight className="h-4 w-4 text-white" /> : 
                              <ArrowUpRight className="h-4 w-4 text-white" />
                            }
                          </div>
                          <span className="text-white">{transaction.type}</span>
                        </div>
                      </td>
                      <td className="py-4 px-4 text-white">{transaction.crypto}</td>
                      <td className={`py-4 px-4 font-medium ${
                        transaction.type === 'واریز' ? 'text-green-400' : 'text-red-400'
                      }`}>
                        {transaction.amount}
                      </td>
                      <td className="py-4 px-4 text-white">{transaction.value} تومان</td>
                      <td className="py-4 px-4 text-gray-400">{transaction.date} {transaction.time}</td>
                      <td className="py-4 px-4">
                        <span className={`px-2 py-1 rounded-full text-xs ${
                          transaction.status === 'تأیید شده' 
                            ? 'bg-green-900 text-green-300' 
                            : 'bg-yellow-900 text-yellow-300'
                        }`}>
                          {transaction.status}
                        </span>
                      </td>
                      <td className="py-4 px-4 text-gray-400 text-sm font-mono">
                        {transaction.txHash.substring(0, 10)}...
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default WalletPage;