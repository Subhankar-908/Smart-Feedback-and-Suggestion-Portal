import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import Loading from '../components/Loading';
import { adminService } from '../services/api';
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import {
  TrendingUp,
  Smile,
  Meh,
  Frown,
  AlertTriangle,
  Lightbulb,
  Sparkles,
  ArrowRight,
  Hash,
  Layers,
  Building,
} from 'lucide-react';

const SENTIMENT_COLORS = {
  Positive: '#10b981',
  Neutral: '#f59e0b',
  Negative: '#f43f5e',
};

const CATEGORY_COLORS = ['#3b82f6', '#6366f1', '#10b981', '#8b5cf6', '#f59e0b', '#ec4899', '#06b6d4', '#f97316', '#64748b'];

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [trends, setTrends] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [statsData, analyticsData, trendsData, alertsData, insightsData] =
          await Promise.all([
            adminService.getDashboardStats(),
            adminService.getAnalytics(),
            adminService.getTrends(),
            adminService.getAlerts(),
            adminService.getInsights(),
          ]);

        setStats(statsData);
        setAnalytics(analyticsData);
        setTrends(trendsData);
        setAlerts(alertsData);
        setInsights(insightsData);
      } catch (err) {
        console.error('Failed to load admin dashboard data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="flex flex-col md:flex-row min-h-[calc(100vh-4rem)] bg-slate-50">
        <Sidebar />
        <main className="flex-1 p-8">
          <Loading message="Compiling real-time NLP analytics and dashboard charts..." />
        </main>
      </div>
    );
  }

  const sentimentData = (analytics?.sentiment_distribution || []).map((item) => ({
    name: item.label,
    value: item.count,
    color: SENTIMENT_COLORS[item.label] || '#94a3b8',
  }));

  const categoryData = (analytics?.category_distribution || []).map((item, idx) => ({
    name: item.category,
    count: item.count,
    fill: CATEGORY_COLORS[idx % CATEGORY_COLORS.length],
  }));

  const deptData = analytics?.department_analysis || [];
  const keywords = analytics?.keywords || [];

  return (
    <div className="flex flex-col md:flex-row min-h-[calc(100vh-4rem)] bg-slate-50">
      <Sidebar />

      <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl">
        {/* Top Header */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
          <div>
            <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-purple-100 text-purple-800 border border-purple-200 mb-1">
              <Sparkles className="w-3.5 h-3.5 text-purple-600" />
              Real-time NLP Insights
            </div>
            <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 tracking-tight">
              Institutional Feedback Analytics
            </h1>
            <p className="text-sm text-gray-500 mt-0.5">
              Automated sentiment analysis, topic categorization, and urgent issue tracking
            </p>
          </div>

          <Link
            to="/admin/feedback"
            className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold px-4 py-2.5 rounded-xl shadow-sm transition-colors"
          >
            Manage Feedback Table <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        {/* Urgent Alerts Banner (if any) */}
        {alerts.length > 0 && (
          <div className="bg-rose-50 border border-rose-200 rounded-2xl p-4 sm:p-5 mb-8 shadow-xs">
            <div className="flex items-center gap-2 text-rose-800 font-bold text-sm mb-2">
              <AlertTriangle className="w-4 h-4 text-rose-600 animate-pulse" />
              {alerts.length} Urgent Issue{alerts.length > 1 ? 's' : ''} Require Immediate Attention
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {alerts.slice(0, 4).map((alert) => (
                <div
                  key={alert.id}
                  className="bg-white p-3 rounded-xl border border-rose-200/80 text-xs shadow-2xs"
                >
                  <div className="flex justify-between items-center font-semibold text-gray-900 mb-1">
                    <span>{alert.course || 'Institutional'}</span>
                    <span className="text-rose-600 font-bold">{alert.category}</span>
                  </div>
                  <p className="text-gray-700 line-clamp-2">"{alert.feedback_text}"</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Key Metrics Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
          <div className="bg-white p-5 rounded-2xl border border-gray-200/80 shadow-xs">
            <div className="flex items-center justify-between text-gray-500 mb-1">
              <span className="text-xs font-semibold uppercase tracking-wider">Total Feedback</span>
              <TrendingUp className="w-4 h-4 text-blue-600" />
            </div>
            <div className="text-2xl sm:text-3xl font-bold text-gray-900">
              {stats?.total_feedback || 0}
            </div>
            <p className="text-xs text-gray-400 mt-1">Across all departments</p>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-gray-200/80 shadow-xs">
            <div className="flex items-center justify-between text-gray-500 mb-1">
              <span className="text-xs font-semibold uppercase tracking-wider">Positive</span>
              <Smile className="w-4 h-4 text-emerald-600" />
            </div>
            <div className="text-2xl sm:text-3xl font-bold text-emerald-600">
              {stats?.positive || 0}
            </div>
            <p className="text-xs text-emerald-600/80 mt-1">
              {stats?.total_feedback
                ? `${Math.round((stats.positive / stats.total_feedback) * 100)}% of total`
                : '0%'}
            </p>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-gray-200/80 shadow-xs">
            <div className="flex items-center justify-between text-gray-500 mb-1">
              <span className="text-xs font-semibold uppercase tracking-wider">Neutral</span>
              <Meh className="w-4 h-4 text-amber-600" />
            </div>
            <div className="text-2xl sm:text-3xl font-bold text-amber-600">
              {stats?.neutral || 0}
            </div>
            <p className="text-xs text-amber-600/80 mt-1">
              {stats?.total_feedback
                ? `${Math.round((stats.neutral / stats.total_feedback) * 100)}% of total`
                : '0%'}
            </p>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-gray-200/80 shadow-xs">
            <div className="flex items-center justify-between text-gray-500 mb-1">
              <span className="text-xs font-semibold uppercase tracking-wider">Negative</span>
              <Frown className="w-4 h-4 text-rose-600" />
            </div>
            <div className="text-2xl sm:text-3xl font-bold text-rose-600">
              {stats?.negative || 0}
            </div>
            <p className="text-xs text-rose-600/80 mt-1">
              {stats?.total_feedback
                ? `${Math.round((stats.negative / stats.total_feedback) * 100)}% of total`
                : '0%'}
            </p>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-gray-200/80 shadow-xs col-span-2 lg:col-span-1">
            <div className="flex items-center justify-between text-gray-500 mb-1">
              <span className="text-xs font-semibold uppercase tracking-wider">Urgent Issues</span>
              <AlertTriangle className="w-4 h-4 text-red-600" />
            </div>
            <div className="text-2xl sm:text-3xl font-bold text-red-600">
              {stats?.urgent_issues || 0}
            </div>
            <p className="text-xs text-red-600/80 mt-1">Requiring action</p>
          </div>
        </div>

        {/* Analytics Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Chart 1: Sentiment Distribution */}
          <div className="bg-white p-6 rounded-2xl border border-gray-200/80 shadow-xs">
            <h3 className="text-base font-bold text-gray-900 mb-1">Sentiment Distribution</h3>
            <p className="text-xs text-gray-500 mb-4">Overall student satisfaction ratio (VADER analysis)</p>
            <div className="h-64 w-full">
              {sentimentData.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={sentimentData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={85}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {sentimentData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-full flex items-center justify-center text-xs text-gray-400">
                  No sentiment data recorded yet
                </div>
              )}
            </div>
          </div>

          {/* Chart 2: Category Distribution */}
          <div className="bg-white p-6 rounded-2xl border border-gray-200/80 shadow-xs">
            <h3 className="text-base font-bold text-gray-900 mb-1">Feedback Categories</h3>
            <p className="text-xs text-gray-500 mb-4">Distribution across key operational areas</p>
            <div className="h-64 w-full">
              {categoryData.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={categoryData} layout="vertical" margin={{ left: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" horizontal={false} />
                    <XAxis type="number" />
                    <YAxis dataKey="name" type="category" width={110} tick={{ fontSize: 12 }} />
                    <Tooltip />
                    <Bar dataKey="count" radius={[0, 6, 6, 0]}>
                      {categoryData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.fill} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-full flex items-center justify-center text-xs text-gray-400">
                  No category data recorded yet
                </div>
              )}
            </div>
          </div>

          {/* Chart 3: Department-wise Feedback Analysis */}
          <div className="bg-white p-6 rounded-2xl border border-gray-200/80 shadow-xs">
            <h3 className="text-base font-bold text-gray-900 mb-1">Department-wise Sentiment</h3>
            <p className="text-xs text-gray-500 mb-4">Sentiment breakdown across academic departments</p>
            <div className="h-64 w-full">
              {deptData.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={deptData}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="department" tick={{ fontSize: 11 }} />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="Positive" stackId="a" fill="#10b981" />
                    <Bar dataKey="Neutral" stackId="a" fill="#f59e0b" />
                    <Bar dataKey="Negative" stackId="a" fill="#f43f5e" />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-full flex items-center justify-center text-xs text-gray-400">
                  No department breakdown available yet
                </div>
              )}
            </div>
          </div>

          {/* Chart 4: Feedback Volume Trends */}
          <div className="bg-white p-6 rounded-2xl border border-gray-200/80 shadow-xs">
            <h3 className="text-base font-bold text-gray-900 mb-1">Submission Trends</h3>
            <p className="text-xs text-gray-500 mb-4">Feedback submission volume over time</p>
            <div className="h-64 w-full">
              {trends.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={trends}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="date" tick={{ fontSize: 11 }} />
                    <YAxis />
                    <Tooltip />
                    <Line
                      type="monotone"
                      dataKey="count"
                      stroke="#3b82f6"
                      strokeWidth={3}
                      dot={{ fill: '#3b82f6', r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-full flex items-center justify-center text-xs text-gray-400">
                  No submission trend data available yet
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Bottom Section: Actionable Insights & Keywords */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Actionable Insights */}
          <div className="lg:col-span-2 bg-white p-6 rounded-2xl border border-gray-200/80 shadow-xs">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded-lg bg-amber-100 text-amber-700 flex items-center justify-center">
                <Lightbulb className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-base font-bold text-gray-900">Actionable Insights & Recommendations</h3>
                <p className="text-xs text-gray-500">Automated administrative advice based on recurring problem areas</p>
              </div>
            </div>

            <div className="space-y-4">
              {insights.length === 0 ? (
                <p className="text-xs text-gray-400 py-4">No critical areas identified yet.</p>
              ) : (
                insights.map((ins, idx) => (
                  <div
                    key={idx}
                    className="p-4 rounded-xl border border-gray-100 bg-slate-50/70 space-y-2"
                  >
                    <div className="flex justify-between items-center">
                      <span className="font-bold text-sm text-gray-900">{ins.category}</span>
                      <span className="text-xs font-semibold text-rose-700 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">
                        {ins.negative_percent}% Negative ({ins.negative_count}/{ins.total_feedback})
                      </span>
                    </div>
                    <p className="text-xs text-gray-600">
                      <strong className="text-gray-800">Frequent Issue:</strong> {ins.common_complaint}
                    </p>
                    <div className="p-2.5 rounded-lg bg-blue-50/80 text-blue-900 text-xs border border-blue-100">
                      <strong>Recommended Action:</strong> {ins.suggested_action}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Frequently Occurring Keywords */}
          <div className="bg-white p-6 rounded-2xl border border-gray-200/80 shadow-xs">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center">
                <Hash className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-base font-bold text-gray-900">Trending Keywords</h3>
                <p className="text-xs text-gray-500">Frequently occurring terms</p>
              </div>
            </div>

            <div className="flex flex-wrap gap-2">
              {keywords.length === 0 ? (
                <p className="text-xs text-gray-400 py-4">No keywords extracted yet.</p>
              ) : (
                keywords.map((kw, idx) => (
                  <span
                    key={idx}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-100 text-slate-800 border border-slate-200 hover:bg-blue-50 hover:text-blue-700 transition-colors"
                  >
                    <span>{kw.word}</span>
                    <span className="bg-slate-200/80 text-slate-700 text-[10px] font-bold px-1.5 py-0.2 rounded-full">
                      {kw.count}
                    </span>
                  </span>
                ))
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default AdminDashboard;
