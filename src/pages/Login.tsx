import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Eye, EyeOff, Shield, Smartphone } from 'lucide-react';

const Login = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [show2FA, setShow2FA] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    twoFACode: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!show2FA) {
      setShow2FA(true);
    } else {
      // Handle final login
      console.log('Login with 2FA:', formData);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="min-h-screen bg-dark-900 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <Shield className="mx-auto h-12 w-12 text-primary-500" />
          <h2 className="mt-6 text-3xl font-bold text-white">
            ورود به حساب کاربری
          </h2>
          <p className="mt-2 text-sm text-gray-400">
            یا{' '}
            <Link
              to="/register"
              className="font-medium text-primary-400 hover:text-primary-300"
            >
              حساب جدید ایجاد کنید
            </Link>
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="bg-dark-800 p-8 rounded-lg shadow-xl">
            {!show2FA ? (
              <>
                <div className="space-y-4">
                  <div>
                    <label htmlFor="email" className="block text-sm font-medium text-gray-300">
                      آدرس ایمیل
                    </label>
                    <input
                      id="email"
                      name="email"
                      type="email"
                      required
                      value={formData.email}
                      onChange={handleChange}
                      className="mt-1 appearance-none relative block w-full px-3 py-2 border border-dark-600 placeholder-gray-400 text-white bg-dark-700 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
                      placeholder="example@email.com"
                    />
                  </div>

                  <div>
                    <label htmlFor="password" className="block text-sm font-medium text-gray-300">
                      رمز عبور
                    </label>
                    <div className="mt-1 relative">
                      <input
                        id="password"
                        name="password"
                        type={showPassword ? 'text' : 'password'}
                        required
                        value={formData.password}
                        onChange={handleChange}
                        className="appearance-none relative block w-full px-3 py-2 pr-10 border border-dark-600 placeholder-gray-400 text-white bg-dark-700 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
                        placeholder="رمز عبور خود را وارد کنید"
                      />
                      <button
                        type="button"
                        className="absolute inset-y-0 right-0 pr-3 flex items-center"
                        onClick={() => setShowPassword(!showPassword)}
                      >
                        {showPassword ? (
                          <EyeOff className="h-5 w-5 text-gray-400" />
                        ) : (
                          <Eye className="h-5 w-5 text-gray-400" />
                        )}
                      </button>
                    </div>
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <input
                        id="remember-me"
                        name="remember-me"
                        type="checkbox"
                        className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-dark-600 rounded bg-dark-700"
                      />
                      <label htmlFor="remember-me" className="mr-2 block text-sm text-gray-300">
                        مرا به خاطر بسپار
                      </label>
                    </div>

                    <div className="text-sm">
                      <a href="#" className="font-medium text-primary-400 hover:text-primary-300">
                        فراموشی رمز عبور؟
                      </a>
                    </div>
                  </div>
                </div>

                <div className="mt-6">
                  <button
                    type="submit"
                    className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
                  >
                    ادامه
                  </button>
                </div>
              </>
            ) : (
              <div className="space-y-4">
                <div className="text-center">
                  <Smartphone className="mx-auto h-12 w-12 text-primary-500 mb-4" />
                  <h3 className="text-lg font-medium text-white">تأیید دو مرحله‌ای</h3>
                  <p className="text-sm text-gray-400 mt-2">
                    کد ۶ رقمی را از اپلیکیشن احراز هویت خود وارد کنید
                  </p>
                </div>

                <div>
                  <label htmlFor="twoFACode" className="block text-sm font-medium text-gray-300">
                    کد تأیید
                  </label>
                  <input
                    id="twoFACode"
                    name="twoFACode"
                    type="text"
                    required
                    maxLength={6}
                    value={formData.twoFACode}
                    onChange={handleChange}
                    className="mt-1 appearance-none relative block w-full px-3 py-2 border border-dark-600 placeholder-gray-400 text-white bg-dark-700 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm text-center text-lg tracking-widest"
                    placeholder="123456"
                  />
                </div>

                <div className="flex space-x-4 space-x-reverse">
                  <button
                    type="button"
                    onClick={() => setShow2FA(false)}
                    className="flex-1 py-2 px-4 border border-dark-600 text-sm font-medium rounded-md text-gray-300 hover:bg-dark-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
                  >
                    بازگشت
                  </button>
                  <button
                    type="submit"
                    className="flex-1 py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
                  >
                    ورود
                  </button>
                </div>

                <div className="text-center">
                  <a href="#" className="text-sm text-primary-400 hover:text-primary-300">
                    کد دریافت نکردید؟
                  </a>
                </div>
              </div>
            )}
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;