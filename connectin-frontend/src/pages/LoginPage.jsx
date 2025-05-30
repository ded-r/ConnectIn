import { useFormik } from "formik";
import * as Yup from "yup";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link, useNavigate, useLocation } from "react-router";
import { faSpinner } from "@fortawesome/free-solid-svg-icons";
import { ReactTyped } from "react-typed";
import { faLightbulb, faHandshakeSimple, faRocket } from "@fortawesome/free-solid-svg-icons";
import { faGoogle, faGithub } from "@fortawesome/free-brands-svg-icons";
import { useEffect } from "react";
import useAuthStore from "../store/authStore";
import OAuthHandler from "../components/OAuthHandler";

const LoginPage = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const { login, loading, handleOAuthCookies } = useAuthStore();

    const validationSchema = Yup.object({
        username: Yup.string().required("Username is required").min(3, "Username must be at least 3 characters long"),
        password: Yup.string().required("Password is required"),
    });

    useEffect(() => {
        // Check for OAuth cookies on component mount
        const authSuccess = handleOAuthCookies();
        if (authSuccess) {
            // Redirect to the page user was trying to access, or home
            const from = location.state?.from || "/";
            navigate(from);
        }
    }, [handleOAuthCookies, navigate, location.state]);

    const formik = useFormik({
        initialValues: {
            username: "",
            password: "",
        },
        validationSchema,
        validateOnBlur: false,
        validateOnChange: true,
        onSubmit: async (values, { setSubmitting }) => {
            const success = await login(values.username, values.password);

            if (success) {
                // Redirect to the page user was trying to access, or home
                const from = location.state?.from || "/";
                navigate(from);
            }

            setSubmitting(false);
        },
    });

    const handleGoogleLogin = () => {
        // Add a loading state indicator if needed
        // setGoogleLoading(true);

        // Store the current path in localStorage to redirect back after login
        const currentPath = location.pathname;
        if (currentPath !== '/login') {
            localStorage.setItem('login_redirect', currentPath);
        }

        // For security, we can add a state parameter
        const state = Math.random().toString(36).substring(2);
        localStorage.setItem('oauth_state', state);
        
        // Use the backend URL directly for production environment
        // This ensures the OAuth callback goes directly to the backend API
        const backendUrl = import.meta.env.PROD 
            ? "https://backend-production-a087.up.railway.app" // Added https:// protocol
            : import.meta.env.VITE_API_URL;
            
        // Redirect to Google OAuth endpoint on the backend
        window.location.href = `${backendUrl}/api/v1/auth/google/login`;
    };

    const handleGithubLogin = () => {
        // Similar implementation to Google login
        // Store redirect info
        const currentPath = location.pathname;
        if (currentPath !== '/login') {
            localStorage.setItem('login_redirect', currentPath);
        }

        // Redirect to GitHub OAuth endpoint
        window.location.href = `${import.meta.env.VITE_API_URL}/auth/github/login`;
    };

    return (
        <div className="flex justify-center items-center min-h-screen -mt-20 px-4">
            {/* This component handles OAuth callbacks */}
            <OAuthHandler />
            
            <div className="flex flex-wrap md:flex-nowrap border border-green-700 dark:border-green-500 rounded-md bg-white dark:bg-gray-800 shadow-lg w-full max-w-3xl">
                {/* Left Side: Form */}
                <div className="flex flex-col flex-1 p-4 sm:p-6">
                    <h1 className="text-lg sm:text-xl font-semibold text-gray-800 dark:text-white mb-2">Welcome!</h1>
                    <p className="text-xs sm:text-sm text-gray-500 dark:text-gray-400 mb-4 sm:mb-6">Sign in to continue your journey!</p>

                    <form onSubmit={formik.handleSubmit} className="space-y-3 sm:space-y-4">
                        {/* Username Field */}
                        <div className="space-y-1 sm:space-y-2">
                            <label htmlFor="username" className="font-semibold text-xs sm:text-sm text-gray-700 dark:text-gray-300">
                                Username
                            </label>
                            <input
                                id="username"
                                type="text"
                                className={`w-full text-xs sm:text-sm px-3 py-2 border rounded-md shadow-sm focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 ${
                                    formik.touched.username && formik.errors.username ? "border-red-500 dark:border-red-500" : "border-gray-300 dark:border-gray-600"
                                }`}
                                placeholder="Enter your username"
                                autoFocus
                                {...formik.getFieldProps("username")}
                            />
                            {formik.touched.username && formik.errors.username && <p className="text-red-500 text-xs mt-1">{formik.errors.username}</p>}
                        </div>

                        {/* Password Field */}
                        <div className="space-y-1 sm:space-y-2">
                            <label htmlFor="password" className="font-semibold text-xs sm:text-sm text-gray-700 dark:text-gray-300">
                                Password
                            </label>
                            <input
                                id="password"
                                type="password"
                                className={`w-full text-xs sm:text-sm px-3 py-2 border rounded-md shadow-sm focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 ${
                                    formik.touched.password && formik.errors.password ? "border-red-500 dark:border-red-500" : "border-gray-300 dark:border-gray-600"
                                }`}
                                placeholder="Enter your password"
                                {...formik.getFieldProps("password")}
                            />
                            {formik.touched.password && formik.errors.password && <p className="text-red-500 text-xs mt-1">{formik.errors.password}</p>}
                        </div>

                        {/* Submit Button */}
                        <div className="mt-4 sm:mt-6">
                            <button
                                type="submit"
                                disabled={formik.isSubmitting || loading}
                                className="w-full font-semibold cursor-pointer shadow-md bg-green-700 dark:bg-green-600 text-white py-2 rounded-md hover:bg-green-600 dark:hover:bg-green-500 transition disabled:bg-green-600 dark:disabled:bg-green-500 disabled:cursor-not-allowed flex items-center justify-center text-sm sm:text-base"
                            >
                                {loading ? (
                                    <>
                                        <FontAwesomeIcon icon={faSpinner} spin className="mr-2" />
                                        Signing in...
                                    </>
                                ) : (
                                    "Sign in"
                                )}
                            </button>
                        </div>

                        {/* Social Login Divider */}
                        <div className="flex items-center my-3">
                            <div className="flex-grow border-t border-gray-300 dark:border-gray-600"></div>
                            <div className="px-3 text-xs text-gray-500 dark:text-gray-400">OR</div>
                            <div className="flex-grow border-t border-gray-300 dark:border-gray-600"></div>
                        </div>

                        {/* Social Login Buttons */}
                        <div className="flex flex-col space-y-2">
                            <button
                                type="button"
                                onClick={handleGoogleLogin}
                                className="w-full flex items-center justify-center gap-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md py-2 text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-600 transition"
                            >
                                <FontAwesomeIcon icon={faGoogle} className="text-red-500" />
                                <span>Continue with Google</span>
                            </button>
                            <button
                                type="button"
                                onClick={handleGithubLogin}
                                className="w-full flex items-center justify-center gap-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md py-2 text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-600 transition"
                            >
                                <FontAwesomeIcon icon={faGithub} className="text-gray-800 dark:text-white" />
                                <span>Continue with GitHub</span>
                            </button>
                        </div>

                        {/* Register Link */}
                        <p className="text-xs sm:text-sm text-center mt-4 sm:mt-6">
                            <span className="text-gray-500 dark:text-gray-400">Don&apos;t have an account?</span>
                            <Link to="/register" className="font-semibold text-green-700 dark:text-green-400 ml-1 hover:underline">
                                Sign up here
                            </Link>
                        </p>
                    </form>
                </div>

                {/* Right Side: Welcome Banner */}
                <div className="bg-gradient-to-br from-green-800 via-green-700 to-green-600 dark:from-green-800 dark:via-green-700 dark:to-green-600 rounded-l-2xl rounded-r-sm flex-1 flex-col justify-center items-center px-4 sm:px-6 py-6 sm:py-8 md:flex hidden">
                    <p className="text-lg sm:text-xl font-semibold text-white">ConnectIn</p>
                    <div className="text-base sm:text-lg mb-4 sm:mb-5 text-white">
                        <ReactTyped strings={["Build Teams.", "Discover Projects.", "Grow Careers.", "Welcome Back!"]} typeSpeed={60} backSpeed={40} loop />
                    </div>
                    <div className="space-y-2 sm:space-y-3 w-full max-w-xs text-white">
                        <div className="flex items-center gap-2 sm:gap-3">
                            <div className="w-5 sm:w-6 flex">
                                <FontAwesomeIcon icon={faLightbulb} className="text-lg sm:text-xl text-yellow-300" />
                            </div>
                            <div>
                                <h3 className="font-semibold text-sm sm:text-base">Innovate Together</h3>
                                <p className="text-xs sm:text-sm">Find projects that ignite your passion.</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-2 sm:gap-3">
                            <div className="w-5 sm:w-6 flex">
                                <FontAwesomeIcon icon={faHandshakeSimple} className="text-lg sm:text-xl text-blue-300" />
                            </div>
                            <div>
                                <h3 className="font-semibold text-sm sm:text-base">Build Connections</h3>
                                <p className="text-xs sm:text-sm">Collaborate with skilled professionals.</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-2 sm:gap-3">
                            <div className="w-5 sm:w-6 flex">
                                <FontAwesomeIcon icon={faRocket} className="text-lg sm:text-xl text-red-300" />
                            </div>
                            <div>
                                <h3 className="font-semibold text-sm sm:text-base">Launch Opportunities</h3>
                                <p className="text-xs sm:text-sm">Discover your next career move.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;
