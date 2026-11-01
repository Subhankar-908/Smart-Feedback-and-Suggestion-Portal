import React, { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';
import Loading from '../components/Loading';
import { adminService, feedbackService } from '../services/api';
import {
  Search,
  Filter,
  Smile,
  Meh,
  Frown,
  AlertTriangle,
  EyeOff,
  User,
  Calendar,
  ChevronLeft,
  ChevronRight,
  RefreshCw,
} from 'lucide-react';

const FeedbackManagement = () => {
  const [feedbacks, setFeedbacks] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  // Filters
  const [departments, setDepartments] = useState([]);
  const [selectedDept, setSelectedDept] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedSentiment, setSelectedSentiment] = useState('');
  const [selectedUrgent, setSelectedUrgent] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  // Pagination
  const [page, setPage] = useState(0);
  const limit = 15;

  const loadDepartments = async () => {
    try {
      const depts = await feedbackService.getDepartments();
      setDepartments(depts);
    } catch (err) {
      console.error('Failed to load departments:', err);
    }
  };

  const fetchFeedback = async () => {
    setLoading(true);
    try {
      const filters = {
        skip: page * limit,
        limit,
      };
      if (selectedDept) filters.department = selectedDept;
      if (selectedCategory) filters.category = selectedCategory;
      if (selectedSentiment) filters.sentiment = selectedSentiment;
      if (selectedUrgent !== '') filters.urgent = selectedUrgent === 'true';
      if (searchQuery.trim()) filters.search = searchQuery.trim();

      const data = await adminService.getFeedbackList(filters);
      setFeedbacks(data.items);
      setTotal(data.total);
    } catch (err) {
      console.error('Failed to load feedback list:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDepartments();
  }, []);

  useEffect(() => {
    fetchFeedback();
  }, [page, selectedDept, selectedCategory, selectedSentiment, selectedUrgent]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setPage(0);
    fetchFeedback();
  };

  const handleResetFilters = () => {
    setSelectedDept('');
    setSelectedCategory('');
    setSelectedSentiment('');
    setSelectedUrgent('');
    setSearchQuery('');
    setPage(0);
  };

  const getSentimentBadge = (label, score) => {
    if (label === 'Positive') {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200">
          <Smile className="w-3.5 h-3.5 text-emerald-600" />
          Positive {score !== null && score !== undefined ? `(${score})` : ''}
        </span>
      );
    }
    if (label === 'Negative') {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-100 text-rose-800 border border-rose-200">
          <Frown className="w-3.5 h-3.5 text-rose-600" />
          Negative {score !== null && score !== undefined ? `(${score})` : ''}
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 border border-amber-200">
        <Meh className="w-3.5 h-3.5 text-amber-600" />
        Neutral {score !== null && score !== undefined ? `(${score})` : ''}
      </span>
    );
  };

  const totalPages = Math.ceil(total / limit);

  return (
    <div className="flex flex-col md:flex-row min-h-[calc(100vh-4rem)] bg-slate-50">
      <Sidebar />

      <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Feedback Management</h1>
            <p className="text-sm text-gray-500 mt-0.5">
              Filter, search, and review all submissions with automated NLP categorizations
            </p>
          </div>

          <button
            onClick={() => fetchFeedback()}
            className="inline-flex items-center gap-1.5 px-3 py-2 bg-white border border-gray-200 hover:bg-gray-50 text-gray-700 text-xs font-semibold rounded-xl transition-colors shadow-2xs"
          >
            <RefreshCw className="w-3.5 h-3.5" /> Refresh List
          </button>
        </div>

        {/* Search & Filter Toolbar */}
        <div className="bg-white p-5 rounded-2xl border border-gray-200/80 shadow-xs mb-6 space-y-4">
          <form onSubmit={handleSearchSubmit} className="flex gap-2">
            <div className="relative flex-1">
              <Search className="w-4 h-4 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search keywords in feedback (e.g. 'computer', 'slow', 'fan')..."
                className="w-full pl-10 pr-4 py-2 bg-gray-50 border border-gray-300 rounded-xl text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white text-gray-900"
              />
            </div>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-xl text-xs sm:text-sm transition-colors"
            >
              Search
            </button>
          </form>

          <div className="flex flex-wrap items-center gap-3 pt-2 border-t border-gray-100">
            <div className="flex items-center gap-1.5 text-xs font-bold text-gray-400 uppercase tracking-wider">
              <Filter className="w-3.5 h-3.5" /> Filters:
            </div>

            <select
              value={selectedDept}
              onChange={(e) => {
                setSelectedDept(e.target.value);
                setPage(0);
              }}
              className="px-3 py-1.5 bg-gray-50 border border-gray-300 rounded-lg text-xs font-medium text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Departments</option>
              {departments.map((d) => (
                <option key={d} value={d}>
                  {d}
                </option>
              ))}
            </select>

            <select
              value={selectedCategory}
              onChange={(e) => {
                setSelectedCategory(e.target.value);
                setPage(0);
              }}
              className="px-3 py-1.5 bg-gray-50 border border-gray-300 rounded-lg text-xs font-medium text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Categories</option>
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

            <select
              value={selectedSentiment}
              onChange={(e) => {
                setSelectedSentiment(e.target.value);
                setPage(0);
              }}
              className="px-3 py-1.5 bg-gray-50 border border-gray-300 rounded-lg text-xs font-medium text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Sentiments</option>
              <option value="Positive">Positive</option>
              <option value="Neutral">Neutral</option>
              <option value="Negative">Negative</option>
            </select>

            <select
              value={selectedUrgent}
              onChange={(e) => {
                setSelectedUrgent(e.target.value);
                setPage(0);
              }}
              className="px-3 py-1.5 bg-gray-50 border border-gray-300 rounded-lg text-xs font-medium text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Urgencies</option>
              <option value="true">Urgent Only</option>
              <option value="false">Non-Urgent</option>
            </select>

            {(selectedDept || selectedCategory || selectedSentiment || selectedUrgent || searchQuery) && (
              <button
                type="button"
                onClick={handleResetFilters}
                className="text-xs text-blue-600 hover:text-blue-800 font-semibold underline ml-auto"
              >
                Reset All Filters
              </button>
            )}
          </div>
        </div>

        {/* Feedback Table */}
        <div className="bg-white rounded-2xl border border-gray-200/80 shadow-xs overflow-hidden">
          {loading ? (
            <div className="p-8">
              <Loading message="Loading feedback records..." />
            </div>
          ) : feedbacks.length === 0 ? (
            <div className="p-12 text-center text-gray-500 text-sm">
              No feedback records matching the selected criteria.
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs sm:text-sm">
                <thead className="bg-gray-50 border-b border-gray-200 text-gray-600 font-semibold uppercase text-[11px] tracking-wider">
                  <tr>
                    <th className="py-3.5 px-4">Date</th>
                    <th className="py-3.5 px-4">Course / Faculty</th>
                    <th className="py-3.5 px-4">Feedback Content</th>
                    <th className="py-3.5 px-4">Category</th>
                    <th className="py-3.5 px-4">Sentiment</th>
                    <th className="py-3.5 px-4">Status</th>
                    <th className="py-3.5 px-4">Submitter</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {feedbacks.map((f) => (
                    <tr key={f.id} className="hover:bg-gray-50/80 transition-colors">
                      <td className="py-3.5 px-4 text-gray-500 whitespace-nowrap">
                        {new Date(f.date).toLocaleDateString(undefined, {
                          month: 'short',
                          day: 'numeric',
                        })}
                      </td>

                      <td className="py-3.5 px-4">
                        <div className="font-semibold text-gray-900">{f.course || 'N/A'}</div>
                        <div className="text-gray-500 text-xs">
                          {f.faculty || f.department || ''}
                        </div>
                      </td>

                      <td className="py-3.5 px-4 max-w-xs md:max-w-md">
                        <p className="text-gray-800 text-xs leading-relaxed line-clamp-3">
                          "{f.feedback_text}"
                        </p>
                      </td>

                      <td className="py-3.5 px-4 whitespace-nowrap">
                        <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-800 border border-slate-200">
                          {f.category || 'Other'}
                        </span>
                      </td>

                      <td className="py-3.5 px-4 whitespace-nowrap">
                        {getSentimentBadge(f.sentiment_label, f.sentiment_score)}
                      </td>

                      <td className="py-3.5 px-4 whitespace-nowrap">
                        {f.urgent ? (
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-bold bg-red-100 text-red-800 border border-red-200">
                            <AlertTriangle className="w-3 h-3 text-red-600" />
                            URGENT
                          </span>
                        ) : (
                          <span className="text-gray-400 text-xs">Normal</span>
                        )}
                      </td>

                      <td className="py-3.5 px-4 whitespace-nowrap">
                        {f.anonymous ? (
                          <span className="inline-flex items-center gap-1 text-purple-700 bg-purple-50 px-2 py-0.5 rounded font-medium text-xs">
                            <EyeOff className="w-3 h-3" /> Anonymous
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 text-gray-700 text-xs font-medium">
                            <User className="w-3 h-3 text-gray-400" />
                            {f.student_name || 'Student'}
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Pagination bar */}
          <div className="p-4 border-t border-gray-100 flex items-center justify-between text-xs text-gray-500">
            <span>
              Showing {feedbacks.length} of {total} results
            </span>

            <div className="flex items-center gap-2">
              <button
                disabled={page === 0}
                onClick={() => setPage((p) => Math.max(0, p - 1))}
                className="p-1.5 rounded-lg border border-gray-200 hover:bg-gray-50 disabled:opacity-40 transition-colors"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <span className="font-semibold text-gray-800">
                Page {page + 1} of {Math.max(1, totalPages)}
              </span>
              <button
                disabled={page + 1 >= totalPages}
                onClick={() => setPage((p) => p + 1)}
                className="p-1.5 rounded-lg border border-gray-200 hover:bg-gray-50 disabled:opacity-40 transition-colors"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default FeedbackManagement;
