import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { UserPlus, Eye, EyeOff, Smartphone, CheckCircle } from 'lucide-react';

const Register = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
    verificationCode: '',
    twoFACode: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (currentStep < 3) {
      setCurrentStep(currentStep + 1);
    } else {
      console.log('Registration complete:', formData);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const steps = [
    { number: 1, title: 'اطلاعات شخصی' },
    { number: 2, title: 'تأیید شماره' },
    { number: 3, title: 'تنظیم 2FA' }
  ];

  return (
    <div className="min-h-screen bg-dark-900 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <UserPlus className="mx-auto h-12 w-12 text-primary-500" />
          <h2 className="mt-6 text-3xl font-bold text-white">
            ایجاد حساب کاربری
          </h2>
          <p className="mt-2 text-sm text-gray-400">
            یا{' '}
            <Link
              to="/login"
              className="font-medium text-primary-400 hover:text-primary-300"
            >
              وارد حساب خود شوید
            </Link>
          </p>
        </div>

        {/* Progress Steps */}
        <div className="flex justify-center">
          <div className="flex items-center space-x-4 space-x-reverse">
            {steps.map((step) => (
              <div key={step.number} className="flex items-center">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                    currentStep >= step.number
                      ? 'bg-primary-600 text-white'
                      : 'bg-dark-700 text-gray-400'
                  }`}
                >
                  {currentStep > step.number ? (
                    <CheckCircle className="h-4 w-4" />
                  ) : (
                    step.number
                  )}
                </div>
                <div className="mr-2 text-xs text-gray-400">{step.title}</div>
                {step.number < steps.length && (
                  <div className="w-8 h-px bg-dark-600 mr-4"></div>
                )}
              </div>
            ))}
          </div>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="bg-dark-800 p-8 rounded-lg shadow-xl">
            {currentStep === 1 && (
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="firstName" className="block text-sm font-medium text-gray-300">
                      نام
                    </label>
                    <input
                      id="firstName"
                      name="firstName"
                      type="text"
                      required
                      value={formData.firstName}
                      onChange={handleChange}
                      className="mt-1 appearance-none relative block w-full px-3 py-2 border border-dark-600 placeholder-gray-400 text-white bg-dark-700 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
                      placeholder="نام"
                    />
                  </div>
                  <div>
                    <label htmlFor="lastName" className="block text-sm font-medium text-gray-300">
                      نام خانوادگی
                    </label>
                    <input
                      id="lastName"
                      name="lastName"
                      type="text"
                      required
                      value={formData.lastName}
                      onChange={handleChange}
                      className="mt-1 appearance-none relative block w-full px-3 py-2 border border-dark-600 placeholder-gray-400 text-white bg-dark-700 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
                      placeholder="نام خانوادگی"
                    />
                  </div>
                </div>

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
                  <label htmlFor="phone" className="block text-sm font-medium text-gray-300">
                    شماره همراه
                  </label>
                  <input
                    id="phone"
                    name="phone"
                    type="tel"
                    required
                    value={formData.phone}
                    onChange={handleChange}
                    className="mt-1 appearance-none relative block w-full px-3 py-2 border border-dark-600 placeholder-gray-400 text-white bg-dark-700 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
                    placeholder="09123456789"
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
                      placeholder="رمز عبور قوی انتخاب کنید"
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

                <div>
                  <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-300">
                    تکرار رمز عبور
                  </label>
                  <div className="mt-1 relative">
                    <input
                      id="confirmPassword"
                      name="confirmPassword"
                      type={showConfirmPassword ? 'text' : 'password'}
                      required
                      value={formData.confirmPassword}
                      onChange={handleChange}
                      className="appearance-none relative block w-full px-3 py-2 pr-10 border border-dark-600 placeholder-gray-400 text-white bg-dark-700 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
                      placeholder="رمز عبور را مجدداً وارد کنید"
                    />
                    <button
                      type="button"
                      className="absolute inset-y-0 right-0 pr-3 flex items-center"
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    >
                      {showConfirmPassword ? (
                        <EyeOff className="h-5 w-5 text-gray-400" />
                      ) : (
                        <Eye className="h-5 w-5 text-gray-400" />
                      )}
                    </button>
                  </div>
                </div>
              </div>
            )}

            {currentStep === 2 && (
              <div className="space-y-4">
                <div className="text-center">
                  <Smartphone className="mx-auto h-12 w-12 text-primary-500 mb-4" />
                  <h3 className="text-lg font-medium text-white">تأیید شماره همراه</h3>
                  <p className="text-sm text-gray-400 mt-2">
                    کد تأیید ارسال شده به شماره {formData.phone} را وارد کنید
                  </p>
                </div>

                <div>
                  <label htmlFor="verificationCode" className="block text-sm font-medium text-gray-300">
                    کد تأیید
                  </label>
                  <input
                    id="verificationCode"
                    name="verificationCode"
                    type="text"
                    required
                    maxLength={6}
                    value={formData.verificationCode}
                    onChange={handleChange}
                    className="mt-1 appearance-none relative block w-full px-3 py-2 border border-dark-600 placeholder-gray-400 text-white bg-dark-700 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm text-center text-lg tracking-widest"
                    placeholder="123456"
                  />
                </div>

                <div className="text-center">
                  <a href="#" className="text-sm text-primary-400 hover:text-primary-300">
                    ارسال مجدد کد (۱:۳۰)
                  </a>
                </div>
              </div>
            )}

            {currentStep === 3 && (
              <div className="space-y-4">
                <div className="text-center">
                  <CheckCircle className="mx-auto h-12 w-12 text-green-500 mb-4" />
                  <h3 className="text-lg font-medium text-white">تنظیم احراز هویت دو مرحله‌ای</h3>
                  <p className="text-sm text-gray-400 mt-2">
                    برای امنیت بیشتر، کد 2FA را از اپلیکیشن احراز هویت خود وارد کنید
                  </p>
                </div>

                <div>
                  <label htmlFor="twoFACode" className="block text-sm font-medium text-gray-300">
                    کد 2FA
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

                <div className="bg-dark-700 p-4 rounded-md">
                  <p className="text-sm text-gray-300">
                    💡 اپلیکیشن‌های پیشنهادی: Google Authenticator، Authy
                  </p>
                </div>
              </div>
            )}

            <div className="mt-6 flex space-x-4 space-x-reverse">
              {currentStep > 1 && (
                <button
                  type="button"
                  onClick={() => setCurrentStep(currentStep - 1)}
                  className="flex-1 py-2 px-4 border border-dark-600 text-sm font-medium rounded-md text-gray-300 hover:bg-dark-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
                >
                  مرحله قبل
                </button>
              )}
              <button
                type="submit"
                className="flex-1 py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
              >
                {currentStep === 3 ? 'تکمیل ثبت نام' : 'مرحله بعد'}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Register;