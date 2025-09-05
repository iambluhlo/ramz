import React from 'react';
import { TrendingUp, TrendingDown, Wallet, Users, DollarSign, Activity } from 'lucide-react';

const Dashboard = () => {
  const stats = [
    {
      title: 'موجودی کل',
      value: '۱۲۵,۰۰۰,۰۰۰',
      unit: 'تومان',
      change: '+۱۲.۵%',
      changeType: 'increase',
      icon: Wallet
    },
    {
      title: 'سود امروز',
      value: '۸,۵۰۰,۰۰۰',
      unit: 'تومان',
      change: '+۸.۲%',
      changeType: 'increase',
      icon: TrendingUp
    },
    {
      title: 'تعداد معاملات',
      value: '۴۷',
      unit: 'معامله',
      change: '+۳.۱%',
      changeType: 'increase',
      icon: Activity
    },
    {
      title: 'ارزش پرتفوی',
      value: '۰.۰۰۴۵',
      unit: 'BTC',
      change: '-۱.۲%',
      changeType: 'decrease',
      icon: DollarSign
    }
  ];

  const recentTransactions = [
    {
      type: 'خرید',
      crypto: 'بیت‌کوین',
      amount: '۰.۰۰۱۲',
      value: '۳,۱۸۰,۰۰۰',
      time: '۲ ساعت پیش',
      status: 'موفق'
    },
    {
      type: 'فروش',
      crypto: 'اتریوم',
      amount: '۰.۰۵',
      value: '۸,۲۵۰,۰۰۰',
      time: '۴ ساعت پیش',
      status: 'موفق'
    },
    {
      type: 'خرید',
      crypto: 'کاردانو',
      amount: '۱۰۰',
      value: '۱,۸۵۰,۰۰۰',
      time: '۶ ساعت پیش',
      status: 'در حال پردازش'
    }
  ];

  const portfolio = [
    {
      crypto: 'بیت‌کوین',
      symbol: 'BTC',
      amount: '۰.۰۰۴۵',
      value: '۱۱۹,۲۵۰,۰۰۰',
      percentage: '۷۵.۲%',
      change: '+۲.۵%'
    },
    {
      crypto: 'اتریوم',
      symbol: 'ETH',
      amount: '۰.۱۲۳',
      value: '۲۰,۲۹۵,۰۰۰',
      percentage: '۱۲.۸%',
      change: '-۱.۲%'
    },
    {
      crypto: 'کاردانو',
      symbol: 'ADA',
      amount: '۸۵۰',
      value: '۱۵,۷۲۵,۰۰۰',
      percentage: '۹.۹%',
      change: '+۵.۸%'
    },
    {
      crypto: 'سولانا',
      symbol: 'SOL',
      amount: '۱.۲۳',
      value: '۳,۳۲۰,۰۰۰',
      percentage: '۲.۱%',
      change: '+۸.۲%'
    }
  ];

  return (
    <div className="min-h-screen bg-dark-900 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">داشبورد</h1>
          <p className="text-gray-400">مرور کلی از پرتفوی و معاملات شما</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <div key={index} className="bg-dark-800 rounded-lg p-6 hover:bg-dark-700 transition-colors">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center">
                  <stat.icon className="h-8 w-8 text-primary-500 ml-3" />
                  <h3 className="text-sm font-medium text-gray-400">{stat.title}</h3>
                </div>
                <span className={`text-sm font-medium ${
                  stat.changeType === 'increase' ? 'text-green-400' : 'text-red-400'
                }`}>
                  {stat.change}
                </span>
              </div>
              <div className="flex items-baseline">
                <span className="text-2xl font-bold text-white">{stat.value}</span>
                <span className="text-sm text-gray-400 mr-2">{stat.unit}</span>
              </div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Portfolio */}
          <div className="bg-dark-800 rounded-lg p-6">
            <h2 className="text-xl font-bold text-white mb-6">پرتفوی</h2>
            <div className="space-y-4">
              {portfolio.map((item, index) => (
                <div key={index} className="flex items-center justify-between p-4 bg-dark-700 rounded-lg hover:bg-dark-600 transition-colors">
                  <div className="flex items-center">
                    <div className="w-10 h-10 bg-primary-600 rounded-full flex items-center justify-center ml-4">
                      <span className="text-white font-bold text-sm">{item.symbol}</span>
                    </div>
                    <div>
                      <h3 className="font-medium text-white">{item.crypto}</h3>
                      <p className="text-sm text-gray-400">{item.amount} {item.symbol}</p>
                    </div>
                  </div>
                  <div className="text-left">
                    <p className="font-medium text-white">{item.value} تومان</p>
                    <div className="flex items-center">
                      <span className="text-sm text-gray-400 ml-2">{item.percentage}</span>
                      <span className={`text-sm font-medium ${
                        item.change.startsWith('+') ? 'text-green-400' : 'text-red-400'
                      }`}>
                        {item.change}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Recent Transactions */}
          <div className="bg-dark-800 rounded-lg p-6">
            <h2 className="text-xl font-bold text-white mb-6">معاملات اخیر</h2>
            <div className="space-y-4">
              {recentTransactions.map((transaction, index) => (
                <div key={index} className="flex items-center justify-between p-4 bg-dark-700 rounded-lg hover:bg-dark-600 transition-colors">
                  <div className="flex items-center">
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center ml-4 ${
                      transaction.type === 'خرید' ? 'bg-green-600' : 'bg-red-600'
                    }`}>
                      {transaction.type === 'خرید' ? 
                        <TrendingUp className="h-5 w-5 text-white" /> : 
                        <TrendingDown className="h-5 w-5 text-white" />
                      }
                    </div>
                    <div>
                      <h3 className="font-medium text-white">{transaction.type} {transaction.crypto}</h3>
                      <p className="text-sm text-gray-400">{transaction.time}</p>
                    </div>
                  </div>
                  <div className="text-left">
                    <p className="font-medium text-white">{transaction.amount}</p>
                    <p className="text-sm text-gray-400">{transaction.value} تومان</p>
                    <span className={`text-xs px-2 py-1 rounded-full ${
                      transaction.status === 'موفق' 
                        ? 'bg-green-900 text-green-300' 
                        : 'bg-yellow-900 text-yellow-300'
                    }`}>
                      {transaction.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mt-8 bg-dark-800 rounded-lg p-6">
          <h2 className="text-xl font-bold text-white mb-6">عملیات سریع</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button className="bg-green-600 hover:bg-green-700 text-white p-4 rounded-lg font-medium transition-colors">
              خرید سریع
            </button>
            <button className="bg-red-600 hover:bg-red-700 text-white p-4 rounded-lg font-medium transition-colors">
              فروش سریع
            </button>
            <button className="bg-primary-600 hover:bg-primary-700 text-white p-4 rounded-lg font-medium transition-colors">
              تبدیل ارز
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;