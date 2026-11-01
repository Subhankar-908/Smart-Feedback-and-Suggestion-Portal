import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import Loading from '../components/Loading';
import { feedbackService } from '../services/api';
import {
  History,
  MessageSquarePlus,
  Smile,
  Meh,
  Frown,
  AlertTriangle,
  Calendar,
  Filter,
  EyeOff,
  User,
} from 'lucide-react';

const FeedbackHistory = () => {
  const [feedbacks, setFeedbacks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterSentiment, setFilterSentiment] = useState('ALL');
  const [filterCategory, setFilterCategory] = useState('ALL');

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await feedbackService.getMyFeedback();
        setFeedbacks(data);
      } catch (err) {
        console.error('Failed to load feedback history:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  const filtered = feedbacks.filter((item) => {
    if (filterSentiment !== 'ALL' && item.sentiment_label !== filterSentiment) {
      return false;
    }
    if (filterCategory !== 'ALL' && item.category !== filterCategory) {
      return false;
    }
    return true;
  });

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
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">My Feedback History</h1>
            <p className="text-sm text-gray-500 mt-0.5">
              Review all feedback you've submitted along with their NLP analysis results.
            </p>
          </div>

          <Link
            to="/student/feedback/new"
            className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold px-4 py-2.5 rounded-xl shadow-sm text-sm transition-colors"
          >
            <MessageSquarePlus className="w-4 h-4" />
            Submit New Feedback
          </Link>
        </div>

        {/* Filters */}
        <div className="bg-white p-4 rounded-xl border border-gray-200/80 shadow-xs mb-6 flex flex-wrap items-center gap-4">
          <div className="flex items-center gap-2 text-xs font-bold text-gray-500 uppercase tracking-wider">
            <Filter className="w-4 h-4" /> Filters:
          </div>

          <select
            value={filterSentiment}
            onChange={(e) => setFilterSentiment(e.target.value)}
            className="px-3 py-1.5 bg-gray-50 border border-gray-300 rounded-lg text-xs font-medium text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="ALL">All Sentiments</option>
            <option value="Positive">Positive</option>
            <option value="Neutral">Neutral</option>
            <option value="Negative">Negative</option>
          </select>

          <select
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
            className="px-3 py-1.5 bg-gray-50 border border-gray-300 rounded-lg text-xs font-medium text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="ALL">All Categories</option>
            <option value="Teaching Pace">Teaching & Academics</option>
            <option value="Lab Facilities">Lab Facilities</option>
            <option value="Canteen & Food">Canteen & Food Quality</option>
            <option value="Placements & Training">Placements & Training</option>
            <option value="College Services & Admin">College Services & Admin</option>
            <option value="Infrastructure & Hostel">Infrastructure & Hostel</option>
            <option value="Library Services">Library Services</option>
            <option value="Syllabus Coverage">Syllabus Coverage</option>
            <option value="Other">Other / General</option>
          </select>

          <div className="text-xs text-gray-400 ml-auto font-medium">
            Showing {filtered.length} of {feedbacks.length}
          </div>
        </div>

        {/* Content list */}
        {loading ? (
          <Loading message="Loading your feedback history..." />
        ) : filtered.length === 0 ? (
          <div className="bg-white rounded-2xl border border-gray-200/80 p-12 text-center">
            <History className="w-10 h-10 text-gray-300 mx-auto mb-3" />
            <h3 className="text-sm font-bold text-gray-800">No matching feedback entries found</h3>
            <p className="text-xs text-gray-500 mt-1">Try changing your filters or submit a new feedback.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {filtered.map((item) => (
              <div
                key={item.id}
                className="bg-white p-5 rounded-2xl border border-gray-200/80 shadow-xs hover:border-gray-300 transition-all"
              >
                <div className="flex flex-wrap items-start justify-between gap-3 mb-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-gray-900 text-sm sm:text-base">
                        {item.course_name || 'General Course'}
                      </span>
                      {item.faculty_name && (
                        <span className="text-xs text-gray-600 bg-gray-100 px-2 py-0.5 rounded font-medium">
                          {item.faculty_name}
                        </span>
                      )}
                    </div>
                    {item.department && (
                      <div className="text-xs text-gray-500 mt-0.5">{item.department}</div>
                    )}
                  </div>

                  <div className="flex items-center gap-2">
                    {item.category && (
                      <span className="px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-100 text-slate-800 border border-slate-200">
                        {item.category}
                      </span>
                    )}
                    {getSentimentBadge(item.sentiment_label)}
                    {item.urgent && (
                      <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-bold bg-rose-100 text-rose-800 border border-rose-200">
                        <AlertTriangle className="w-3.5 h-3.5 text-rose-600" />
                        Urgent
                      </span>
                    )}
                  </div>
                </div>

                <div className="bg-gray-50/80 p-3.5 rounded-xl border border-gray-100 text-sm text-gray-800 leading-relaxed">
                  "{item.feedback_text}"
                </div>

                <div className="mt-3.5 flex items-center justify-between text-xs text-gray-400">
                  <span className="flex items-center gap-1.5">
                    <Calendar className="w-3.5 h-3.5" />
                    Submitted on{' '}
                    {new Date(item.created_at).toLocaleDateString(undefined, {
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric',
                    })}
                  </span>

                  {item.anonymous ? (
                    <span className="flex items-center gap-1 text-purple-600 font-semibold bg-purple-50 px-2.5 py-0.5 rounded-md">
                      <EyeOff className="w-3.5 h-3.5" /> Anonymous Submission
                    </span>
                  ) : (
                    <span className="flex items-center gap-1 text-gray-500 font-medium">
                      <User className="w-3.5 h-3.5" /> Public Submission
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
};

export default FeedbackHistory;
