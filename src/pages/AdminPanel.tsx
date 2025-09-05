import React, { useState } from 'react';
import { Users, TrendingUp, DollarSign, AlertTriangle, Settings, Shield, Activity, BarChart3 } from 'lucide-react';

const AdminPanel = () => {
  const [activeTab, setActiveTab] = useState('dashboard');

  const adminStats = [
    {
      title: 'کل کاربران',
      value: '12,856',
      change: '+5.2%',
      changeType: 'increase',
      icon: Users
    },
    {
      title: 'حجم معاملات روزانه',
      value: '2.8B',
      change: '+12.5%',
      changeType: 'increase',
      icon: TrendingUp
    },
    {
      title: 'درآمد',
      value: '850M',
      change: '+8.1%',
      changeType: 'increase',
      icon: DollarSign
    },
    {
      title: 'هشدارهای امنیتی',
      value: '3',
      change: '-50%',
      changeType: 'decrease',
      icon: AlertTriangle
    }
  ];

  const recentUsers = [
    {
      name: 'علی احمدی',
      email: 'ali.ahmadi@email.com',
      status: 'فعال',
      joined: '۱۴۰۲/۰۹/۱۵',
      balance: '12,500,000'
    },
    {
      name: 'مریم کریمی',
      email: 'maryam.karimi@email.com',
      status: 'در انتظار تأیید',
      joined: '۱۴۰۲/۰۹/۱۴',
      balance: '5,200,000'
    },
    {
      name: 'حسن محمدی',
      email: 'hasan.mohammadi@email.com',
      status: 'فعال',
      joined: '۱۴۰۲/۰۹/۱۳',
      balance: '28,750,000'
    },
    {
      name: 'فاطمه زارعی',
      email: 'fateme.zarei@email.com',
      status: 'مسدود',
      joined: '۱۴۰۲/۰۹/۱۲',
      balance: '850,000'
    }
  ];

  const systemAlerts = [
    {
      type: 'امنیتی',
      message: 'تلاش ورود مشکوک از IP: 192.168.1.100',
      time: '۱۰ دقیقه پیش',
      severity: 'high'
    },
    {
      type: 'سیستم',
      message: 'استفاده از CPU بالاتر از 85%',
      time: '۳۰ دقیقه پیش',
      severity: 'medium'
    },
    {
      type: 'معاملات',
      message: 'حجم معاملات غیرعادی در BTC',
      time: '۱ ساعت پیش',
      severity: 'low'
    }
  ];

  const tabs = [
    { id: 'dashboard', label: 'داشبورد', icon: BarChart3 },
    { id: 'users', label: 'کاربران', icon: Users },
    { id: 'transactions', label: 'معاملات', icon: Activity },
    { id: 'settings', label: 'تنظیمات', icon: Settings },
    { id: 'security', label: 'امنیت', icon: Shield },
  ];

  return (
    <div className="min-h-screen bg-dark-900 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">پنل مدیریت</h1>
          <p className="text-gray-400">مدیریت سیستم و نظارت بر عملکرد</p>
        </div>

        {/* Navigation Tabs */}
        <div className="flex border-b border-dark-700 mb-8 overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center space-x-2 space-x-reverse py-4 px-6 font-medium transition-colors whitespace-nowrap ${
                activeTab === tab.id
                  ? 'border-b-2 border-primary-500 text-primary-500'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              <tab.icon className="h-5 w-5" />
              <span>{tab.label}</span>
            </button>
          ))}
        </div>

        {/* Dashboard Tab */}
        {activeTab === 'dashboard' && (
          <div className="space-y-8">
            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {adminStats.map((stat, index) => (
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
                  </div>
                </div>
              ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Recent Users */}
              <div className="bg-dark-800 rounded-lg p-6">
                <h2 className="text-xl font-bold text-white mb-6">کاربران اخیر</h2>
                <div className="space-y-4">
                  {recentUsers.map((user, index) => (
                    <div key={index} className="flex items-center justify-between p-4 bg-dark-700 rounded-lg hover:bg-dark-600 transition-colors">
                      <div className="flex items-center">
                        <div className="w-10 h-10 bg-primary-600 rounded-full flex items-center justify-center ml-4">
                          <span className="text-white font-bold text-sm">{user.name.charAt(0)}</span>
                        </div>
                        <div>
                          <h3 className="font-medium text-white">{user.name}</h3>
                          <p className="text-sm text-gray-400">{user.email}</p>
                        </div>
                      </div>
                      <div className="text-left">
                        <span className={`text-xs px-2 py-1 rounded-full ${
                          user.status === 'فعال' ? 'bg-green-900 text-green-300' :
                          user.status === 'در انتظار تأیید' ? 'bg-yellow-900 text-yellow-300' :
                          'bg-red-900 text-red-300'
                        }`}>
                          {user.status}
                        </span>
                        <p className="text-sm text-gray-400 mt-1">{user.joined}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* System Alerts */}
              <div className="bg-dark-800 rounded-lg p-6">
                <h2 className="text-xl font-bold text-white mb-6">هشدارهای سیستم</h2>
                <div className="space-y-4">
                  {systemAlerts.map((alert, index) => (
                    <div key={index} className="flex items-start justify-between p-4 bg-dark-700 rounded-lg">
                      <div className="flex items-start">
                        <div className={`w-3 h-3 rounded-full mt-2 ml-3 ${
                          alert.severity === 'high' ? 'bg-red-500' :
                          alert.severity === 'medium' ? 'bg-yellow-500' :
                          'bg-green-500'
                        }`}></div>
                        <div>
                          <h3 className="font-medium text-white">{alert.type}</h3>
                          <p className="text-sm text-gray-400 mt-1">{alert.message}</p>
                        </div>
                      </div>
                      <span className="text-xs text-gray-400 whitespace-nowrap">{alert.time}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Users Tab */}
        {activeTab === 'users' && (
          <div className="bg-dark-800 rounded-lg p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-white">مدیریت کاربران</h2>
              <div className="flex space-x-4 space-x-reverse">
                <select className="bg-dark-700 border border-dark-600 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500">
                  <option>همه کاربران</option>
                  <option>فعال</option>
                  <option>غیرفعال</option>
                  <option>مسدود</option>
                </select>
                <button className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-md font-medium transition-colors">
                  افزودن کاربر
                </button>
              </div>
            </div>
            
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-dark-600">
                    <th className="text-right py-3 px-4 text-sm font-medium text-gray-400">کاربر</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-gray-400">ایمیل</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-gray-400">وضعیت</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-gray-400">تاریخ عضویت</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-gray-400">موجودی</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-gray-400">عملیات</th>
                  </tr>
                </thead>
                <tbody>
                  {recentUsers.map((user, index) => (
                    <tr key={index} className="border-b border-dark-700 hover:bg-dark-700 transition-colors">
                      <td className="py-4 px-4">
                        <div className="flex items-center">
                          <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center ml-3">
                            <span className="text-white font-bold text-sm">{user.name.charAt(0)}</span>
                          </div>
                          <span className="text-white">{user.name}</span>
                        </div>
                      </td>
                      <td className="py-4 px-4 text-gray-400">{user.email}</td>
                      <td className="py-4 px-4">
                        <span className={`px-2 py-1 rounded-full text-xs ${
                          user.status === 'فعال' ? 'bg-green-900 text-green-300' :
                          user.status === 'در انتظار تأیید' ? 'bg-yellow-900 text-yellow-300' :
                          'bg-red-900 text-red-300'
                        }`}>
                          {user.status}
                        </span>
                      </td>
                      <td className="py-4 px-4 text-gray-400">{user.joined}</td>
                      <td className="py-4 px-4 text-white">{user.balance} تومان</td>
                      <td className="py-4 px-4">
                        <div className="flex space-x-2 space-x-reverse">
                          <button className="text-primary-400 hover:text-primary-300 text-sm">
                            ویرایش
                          </button>
                          <button className="text-red-400 hover:text-red-300 text-sm">
                            مسدود
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Transactions Tab */}
        {activeTab === 'transactions' && (
          <div className="bg-dark-800 rounded-lg p-6">
            <h2 className="text-xl font-bold text-white mb-6">مدیریت معاملات</h2>
            <div className="text-center py-12">
              <Activity className="h-16 w-16 text-gray-500 mx-auto mb-4" />
              <p className="text-gray-400">بخش مدیریت معاملات در حال توسعه است</p>
            </div>
          </div>
        )}

        {/* Settings Tab */}
        {activeTab === 'settings' && (
          <div className="bg-dark-800 rounded-lg p-6">
            <h2 className="text-xl font-bold text-white mb-6">تنظیمات سیستم</h2>
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    نام پلتفرم
                  </label>
                  <input
                    type="text"
                    value="بیت‌کوین پلاس"
                    className="w-full bg-dark-700 border border-dark-600 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    حد مجاز کارمزد (%)
                  </label>
                  <input
                    type="number"
                    value="0.1"
                    step="0.01"
                    className="w-full bg-dark-700 border border-dark-600 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  حد مجاز روزانه برداشت (تومان)
                </label>
                <input
                  type="number"
                  value="500000000"
                  className="w-full bg-dark-700 border border-dark-600 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>

              <div className="flex items-center justify-between">
                <span className="text-white">فعال‌سازی احراز هویت دو مرحله‌ای اجباری</span>
                <button className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors">
                  فعال
                </button>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-white">نمایش هشدار نگهداری</span>
                <button className="bg-dark-600 hover:bg-dark-500 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors">
                  غیرفعال
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Security Tab */}
        {activeTab === 'security' && (
          <div className="bg-dark-800 rounded-lg p-6">
            <h2 className="text-xl font-bold text-white mb-6">تنظیمات امنیتی</h2>
            <div className="space-y-6">
              <div className="bg-dark-700 p-4 rounded-lg">
                <h3 className="text-lg font-medium text-white mb-3">لاگ‌های امنیتی</h3>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-300">تلاش ورود ناموفق</span>
                    <span className="text-red-400">1,234 مورد</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-300">IP های مسدود شده</span>
                    <span className="text-yellow-400">45 مورد</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-300">تراکنش‌های مشکوک</span>
                    <span className="text-green-400">12 مورد</span>
                  </div>
                </div>
              </div>

              <div className="bg-dark-700 p-4 rounded-lg">
                <h3 className="text-lg font-medium text-white mb-3">تنظیمات فایروال</h3>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-300">محدودیت نرخ درخواست</span>
                    <button className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm transition-colors">
                      فعال
                    </button>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-300">فیلتر کشورها</span>
                    <button className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm transition-colors">
                      فعال
                    </button>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-300">تشخیص DDoS</span>
                    <button className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm transition-colors">
                      فعال
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminPanel;