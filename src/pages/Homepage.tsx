import React from 'react';
import { Link } from 'react-router-dom';
import { TrendingUp, Shield, Users, Zap, ArrowLeft } from 'lucide-react';

const Homepage = () => {
  const cryptoPrices = [
    { name: 'بیت‌کوین', symbol: 'BTC', price: '2,650,000,000', change: '+2.5%', changeColor: 'text-green-400' },
    { name: 'اتریوم', symbol: 'ETH', price: '165,000,000', change: '-1.2%', changeColor: 'text-red-400' },
    { name: 'تتر', symbol: 'USDT', price: '42,000', change: '+0.1%', changeColor: 'text-green-400' },
    { name: 'کاردانو', symbol: 'ADA', price: '18,500', change: '+5.8%', changeColor: 'text-green-400' },
    { name: 'پولکادات', symbol: 'DOT', price: '285,000', change: '-3.1%', changeColor: 'text-red-400' },
    { name: 'سولانا', symbol: 'SOL', price: '4,200,000', change: '+8.2%', changeColor: 'text-green-400' },
  ];

  const features = [
    {
      icon: Shield,
      title: 'امنیت بالا',
      description: 'استفاده از جدیدترین تکنولوژی‌های امنیتی و رمزنگاری'
    },
    {
      icon: Zap,
      title: 'سرعت بالا',
      description: 'اجرای فوری سفارشات و پردازش سریع تراکنش‌ها'
    },
    {
      icon: Users,
      title: 'پشتیبانی ۲۴/۷',
      description: 'تیم پشتیبانی حرفه‌ای در تمام ساعات شبانه‌روز'
    },
    {
      icon: TrendingUp,
      title: 'ابزارهای پیشرفته',
      description: 'نمودارهای تکنیکال و ابزارهای تحلیل بازار'
    }
  ];

  return (
    <div className="min-h-screen bg-dark-900">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary-900/20 to-secondary-900/20"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center animate-slide-up">
            <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
              بهترین پلتفرم
              <span className="text-primary-400 block mt-2">معاملات ارزهای دیجیتال</span>
            </h1>
            <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
              با امنیت بالا، سرعت فوق‌العاده و کارمزدهای رقابتی، بهترین تجربه معاملات ارزهای دیجیتال را داشته باشید
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/register"
                className="bg-primary-600 hover:bg-primary-700 text-white px-8 py-3 rounded-lg text-lg font-semibold transition-all duration-200 transform hover:scale-105 animate-pulse-glow"
              >
                شروع معاملات
              </Link>
              <Link
                to="/trading"
                className="border border-primary-500 text-primary-400 hover:bg-primary-500 hover:text-white px-8 py-3 rounded-lg text-lg font-semibold transition-all duration-200 transform hover:scale-105"
              >
                مشاهده بازار
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Market Overview */}
      <section className="py-16 bg-dark-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-white mb-4">بازار ارزهای دیجیتال</h2>
            <p className="text-gray-400">آخرین قیمت‌ها و تغییرات بازار</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {cryptoPrices.map((crypto, index) => (
              <div
                key={crypto.symbol}
                className="bg-dark-700 rounded-lg p-6 hover:bg-dark-600 transition-colors cursor-pointer"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-white">{crypto.name}</h3>
                    <p className="text-gray-400">{crypto.symbol}</p>
                  </div>
                  <div className="w-12 h-12 bg-primary-600 rounded-full flex items-center justify-center">
                    <TrendingUp className="h-6 w-6 text-white" />
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-2xl font-bold text-white">{crypto.price}</span>
                  <span className={`text-sm font-medium ${crypto.changeColor}`}>
                    {crypto.change}
                  </span>
                </div>
                <p className="text-xs text-gray-400 mt-2">تومان</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-dark-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-white mb-4">چرا بیت‌کوین پلاس؟</h2>
            <p className="text-gray-400">امکانات و مزایای منحصر به فرد پلتفرم ما</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="text-center group hover:transform hover:scale-105 transition-all duration-300"
              >
                <div className="w-16 h-16 bg-primary-600 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-primary-500 transition-colors">
                  <feature.icon className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-2">{feature.title}</h3>
                <p className="text-gray-400">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-r from-primary-600 to-secondary-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            همین الان شروع کنید
          </h2>
          <p className="text-xl text-primary-100 mb-8">
            ثبت نام کنید و اولین معامله خود را انجام دهید
          </p>
          <Link
            to="/register"
            className="inline-flex items-center bg-white text-primary-600 px-8 py-3 rounded-lg text-lg font-semibold hover:bg-gray-100 transition-colors space-x-2 space-x-reverse"
          >
            <span>ثبت نام رایگان</span>
            <ArrowLeft className="h-5 w-5" />
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Homepage;