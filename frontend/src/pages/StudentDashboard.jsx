import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { feedbackService } from '../services/api';
import Sidebar from '../components/Sidebar';
import Loading from '../components/Loading';
import {
  MessageSquarePlus,
  History,
  TrendingUp,
  Smile,
  Meh,
  Frown,
  AlertTriangle,
  Clock,
  CheckCircle2,
  Calendar,
} from 'lucide-react';

const StudentDashboard = () => {
  const { user } = useAuth();
  const [feedbacks, setFeedbacks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await feedbackService.getMyFeedback();
        setFeedbacks(data);
      } catch (err) {
        console.error('Failed to load student feedback history:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  const total = feedbacks.length;
  const positive = feedbacks.filter((f) => f.sentiment_label === 'Positive').length;
  const neutral = feedbacks.filter((f) => f.sentiment_label === 'Neutral').length;
  const negative = feedbacks.filter((f) => f.sentiment_label === 'Negative').length;

  const getSentimentBadge = (label) => {
    if (label === 'Positive') {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200">
          <Smile className="w-3.5 h-3.5 text-emerald-600" />
          Positive
        </span>
      );
    }
    if (label === 'Negative') {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-100 text-rose-800 border border-rose-200">
          <Frown className="w-3.5 h-3.5 text-rose-600" />
          Negative
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 border border-amber-200">
        <Meh className="w-3.5 h-3.5 text-amber-600" />
        Neutral
      </span>
    );
  };

  return (
    <div className="flex flex-col md:flex-row min-h-[calc(100vh-4rem)] bg-slate-50">
      <Sidebar />

      <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-6xl">
        {/* Welcome Header */}
        <div className="bg-gradient-to-r from-blue-600 via-indigo-600 to-blue-700 rounded-2xl p-6 sm:p-8 text-white shadow-md shadow-blue-500/15 mb-8">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
              <h1 className="text-2xl sm:text-3xl font-bold tracking-tight">
                Welcome back, {user?.name}! 👋
              </h1>
              <p className="text-blue-100 text-sm sm:text-base mt-1 max-w-xl">
                {user?.department} • Semester {user?.semester || 'N/A'} • Student Portal
              </p>
            </div>

            <div className="flex flex-wrap gap-2.5">
              <Link
                to="/student/feedback/new"
                className="inline-flex items-center gap-2 bg-white text-blue-600 hover:bg-blue-50 font-semibold px-4 py-2.5 rounded-xl shadow-sm text-sm transition-colors"
              >
                <MessageSquarePlus className="w-4 h-4" />
                Give Feedback
              </Link>
              <Link
                to="/student/history"
                className="inline-flex items-center gap-2 bg-blue-500/40 hover:bg-blue-500/60 text-white font-semibold px-4 py-2.5 rounded-xl text-sm border border-white/20 transition-colors"
              >
                <History className="w-4 h-4" />
                View History
              </Link>
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div className="bg-white p-5 rounded-2xl border border-gray-200/80 shadow-xs">
            <div className="flex items-center justify-between text-gray-500 mb-2">
              <span className="text-xs font-semibold uppercase tracking-wider">Total Submitted</span>
              <TrendingUp className="w-4 h-4 text-blue-600" />
            </div>
            <div className="text-2xl sm:text-3xl font-bold text-gray-900">{total}</div>
            <p className="text-xs text-gray-500 mt-1">Lifetime submissions</p>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-gray-200/80 shadow-xs">
            <div className="flex items-center justify-between text-gray-500 mb-2">
              <span className="text-xs font-semibold uppercase tracking-wider">Positive</span>
              <Smile className="w-4 h-4 text-emerald-600" />
            </div>
            <div className="text-2xl sm:text-3xl font-bold text-emerald-600">{positive}</div>
            <p className="text-xs text-gray-500 mt-1">Appreciations</p>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-gray-200/80 shadow-xs">
            <div className="flex items-center justify-between text-gray-500 mb-2">
              <span className="text-xs font-semibold uppercase tracking-wider">Neutral</span>
              <Meh className="w-4 h-4 text-amber-600" />
            </div>
            <div className="text-2xl sm:text-3xl font-bold text-amber-600">{neutral}</div>
            <p className="text-xs text-gray-500 mt-1">General feedback</p>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-gray-200/80 shadow-xs">
            <div className="flex items-center justify-between text-gray-500 mb-2">
              <span className="text-xs font-semibold uppercase tracking-wider">Negative / Issues</span>
              <Frown className="w-4 h-4 text-rose-600" />
            </div>
            <div className="text-2xl sm:text-3xl font-bold text-rose-600">{negative}</div>
            <p className="text-xs text-gray-500 mt-1">Areas of concern</p>
          </div>
        </div>

        {/* Recent Feedback Section */}
        <div className="bg-white rounded-2xl border border-gray-200/80 shadow-xs p-6">
          <div className="flex items-center justify-between mb-5">
            <div>
              <h2 className="text-lg font-bold text-gray-900">Recent Submissions</h2>
              <p className="text-xs text-gray-500">Your most recent feedback entries and their NLP classifications</p>
            </div>
            <Link
              to="/student/history"
              className="text-xs font-semibold text-blue-600 hover:text-blue-700 flex items-center gap-1"
            >
              See all ({total})
            </Link>
          </div>

          {loading ? (
            <Loading message="Loading feedback history..." />
          ) : feedbacks.length === 0 ? (
            <div className="text-center py-12 px-4">
              <div className="w-12 h-12 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center mx-auto mb-3">
                <MessageSquarePlus className="w-6 h-6" />
              </div>
              <h3 className="text-sm font-bold text-gray-900">No feedback submitted yet</h3>
              <p className="text-xs text-gray-500 mt-1 max-w-sm mx-auto">
                Help your institution improve courses, labs, and facilities by submitting your first feedback.
              </p>
              <Link
                to="/student/feedback/new"
                className="mt-4 inline-flex items-center gap-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold px-4 py-2 rounded-xl transition-colors shadow-xs"
              >
                <MessageSquarePlus className="w-3.5 h-3.5" />
                Submit Feedback Now
              </Link>
            </div>
          ) : (
            <div className="space-y-3.5">
              {feedbacks.slice(0, 5).map((f) => (
                <div
                  key={f.id}
                  className="p-4 rounded-xl border border-gray-100 bg-gray-50/50 hover:bg-gray-50 transition-colors"
                >
                  <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold text-gray-800">
                        {f.course_name || 'General Course'}
                      </span>
                      {f.faculty_name && (
                        <span className="text-xs text-gray-500">• {f.faculty_name}</span>
                      )}
                    </div>
                    <div className="flex items-center gap-2">
                      {f.category && (
                        <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-slate-200 text-slate-700">
                          {f.category}
                        </span>
                      )}
                      {getSentimentBadge(f.sentiment_label)}
                      {f.urgent && (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-bold bg-red-100 text-red-800 border border-red-200 animate-pulse">
                          <AlertTriangle className="w-3 h-3 text-red-600" />
                          URGENT
                        </span>
                      )}
                    </div>
                  </div>

                  <p className="text-xs sm:text-sm text-gray-700 line-clamp-2 leading-relaxed">
                    "{f.feedback_text}"
                  </p>

                  <div className="mt-2.5 flex items-center justify-between text-[11px] text-gray-400">
                    <span className="flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      {new Date(f.created_at).toLocaleDateString(undefined, {
                        year: 'numeric',
                        month: 'short',
                        day: 'numeric',
                      })}
                    </span>
                    {f.anonymous ? (
                      <span className="text-purple-600 font-medium bg-purple-50 px-2 py-0.5 rounded">
                        Submitted Anonymously
                      </span>
                    ) : (
                      <span className="text-gray-500">Public Submission</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default StudentDashboard;
