import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import { feedbackService } from '../services/api';
import {
  Send,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  EyeOff,
  Sparkles,
  Smile,
  Frown,
  Meh,
  AlertTriangle,
  ArrowLeft,
  GraduationCap,
  FlaskConical,
  UtensilsCrossed,
  Briefcase,
  Building2,
  Home,
  BookOpen,
  Layers,
} from 'lucide-react';

const CATEGORY_OPTIONS = [
  {
    id: 'Teaching Pace',
    label: 'Teaching & Academics',
    description: 'Faculty lectures, pace, doubt solving & explanations',
    icon: GraduationCap,
    color: 'text-blue-600 bg-blue-50 border-blue-200',
  },
  {
    id: 'Lab Facilities',
    label: 'Lab & Practical Facilities',
    description: 'Computers, software, instruments & coding equipment',
    icon: FlaskConical,
    color: 'text-indigo-600 bg-indigo-50 border-indigo-200',
  },
  {
    id: 'Canteen & Food',
    label: 'Canteen & Food Quality',
    description: 'Cafeteria meals, snacks, hygiene & drinking water',
    icon: UtensilsCrossed,
    color: 'text-emerald-600 bg-emerald-50 border-emerald-200',
  },
  {
    id: 'Placements & Training',
    label: 'Placements & Training',
    description: 'TPO cell, company drives, aptitude & mock interviews',
    icon: Briefcase,
    color: 'text-purple-600 bg-purple-50 border-purple-200',
  },
  {
    id: 'College Services & Admin',
    label: 'College Services & Admin',
    description: 'Administrative office, accounts, fee counter & bus transport',
    icon: Building2,
    color: 'text-amber-600 bg-amber-50 border-amber-200',
  },
  {
    id: 'Infrastructure & Hostel',
    label: 'Infrastructure & Hostel',
    description: 'Classrooms, benches, fans/AC, washrooms & hostel rooms',
    icon: Home,
    color: 'text-rose-600 bg-rose-50 border-rose-200',
  },
  {
    id: 'Library Services',
    label: 'Library & Study Resources',
    description: 'Books, reading rooms, digital journals & issue desk',
    icon: BookOpen,
    color: 'text-teal-600 bg-teal-50 border-teal-200',
  },
  {
    id: 'Auto-Detect',
    label: 'Auto-Detect with AI (General)',
    description: 'Let the NLP pipeline automatically classify your feedback',
    icon: Sparkles,
    color: 'text-slate-600 bg-slate-50 border-slate-200',
  },
];

const FeedbackForm = () => {
  const [selectedCategory, setSelectedCategory] = useState('Teaching Pace');
  const [departments, setDepartments] = useState([]);
  const [selectedDept, setSelectedDept] = useState('');
  const [courses, setCourses] = useState([]);
  const [facultyList, setFacultyList] = useState([]);

  const [courseId, setCourseId] = useState('');
  const [facultyId, setFacultyId] = useState('');
  const [feedbackText, setFeedbackText] = useState('');
  const [isAnonymous, setIsAnonymous] = useState(false);

  const [loadingOptions, setLoadingOptions] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [nlpResultModal, setNlpResultModal] = useState(null);

  const navigate = useNavigate();

  // Load departments on mount
  useEffect(() => {
    const initData = async () => {
      try {
        const depts = await feedbackService.getDepartments();
        setDepartments(depts);
        if (depts.length > 0) {
          setSelectedDept(depts[0]);
        }
      } catch (err) {
        console.error('Failed to load departments:', err);
      } finally {
        setLoadingOptions(false);
      }
    };
    initData();
  }, []);

  // Load courses and faculty whenever department changes
  useEffect(() => {
    const loadDeptOptions = async () => {
      if (!selectedDept) return;
      try {
        const [cList, fList] = await Promise.all([
          feedbackService.getCourses(selectedDept),
          feedbackService.getFaculty(selectedDept),
        ]);
        setCourses(cList);
        setFacultyList(fList);
        if (cList.length > 0) setCourseId(cList[0].id.toString());
        else setCourseId('');
        if (fList.length > 0) setFacultyId(fList[0].id.toString());
        else setFacultyId('');
      } catch (err) {
        console.error('Failed to load courses/faculty:', err);
      }
    };
    loadDeptOptions();
  }, [selectedDept]);

  const isAcademicCategory =
    selectedCategory === 'Teaching Pace' ||
    selectedCategory === 'Lab Facilities' ||
    selectedCategory === 'Auto-Detect';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (feedbackText.trim().length < 10) {
      setError('Feedback text must be at least 10 characters long.');
      return;
    }

    setIsSubmitting(true);

    try {
      const payload = {
        course_id: courseId ? parseInt(courseId, 10) : null,
        faculty_id: facultyId ? parseInt(facultyId, 10) : null,
        category: selectedCategory === 'Auto-Detect' ? null : selectedCategory,
        feedback_text: feedbackText.trim(),
        anonymous: isAnonymous,
      };

      const res = await feedbackService.submitFeedback(payload);
      // Show instant NLP analysis modal
      setNlpResultModal(res);
    } catch (err) {
      const msg = err.response?.data?.detail || 'Failed to submit feedback. Please try again.';
      setError(msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCloseModal = () => {
    setNlpResultModal(null);
    navigate('/student/dashboard');
  };

  return (
    <div className="flex flex-col md:flex-row min-h-[calc(100vh-4rem)] bg-slate-50">
      <Sidebar />

      <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-4xl">
        <div className="mb-6">
          <button
            onClick={() => navigate(-1)}
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-gray-500 hover:text-gray-900 transition-colors mb-2"
          >
            <ArrowLeft className="w-3.5 h-3.5" /> Back
          </button>
          <h1 className="text-2xl font-bold text-gray-900">Submit Institutional Feedback</h1>
          <p className="text-sm text-gray-500 mt-0.5">
            Choose a feedback category (Departmental, Canteen, Placements, Services, etc.) and share your review.
          </p>
        </div>

        <div className="bg-white rounded-2xl border border-gray-200/80 shadow-xs p-6 sm:p-8">
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 text-sm rounded-xl flex items-start gap-2.5">
              <AlertCircle className="w-5 h-5 text-red-600 shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Step 1: Category Selection Cards */}
            <div>
              <label className="block text-xs font-semibold text-gray-700 uppercase tracking-wider mb-2.5">
                1. Select Feedback Category *
              </label>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                {CATEGORY_OPTIONS.map((cat) => {
                  const Icon = cat.icon;
                  const isSelected = selectedCategory === cat.id;
                  return (
                    <button
                      key={cat.id}
                      type="button"
                      onClick={() => setSelectedCategory(cat.id)}
                      className={`p-3.5 rounded-xl border text-left transition-all flex flex-col justify-between ${
                        isSelected
                          ? 'border-blue-600 bg-blue-50/70 ring-2 ring-blue-500/20 shadow-xs'
                          : 'border-gray-200 hover:border-gray-300 bg-white'
                      }`}
                    >
                      <div className="flex items-center justify-between mb-2">
                        <div
                          className={`w-8 h-8 rounded-lg flex items-center justify-center ${cat.color}`}
                        >
                          <Icon className="w-4 h-4" />
                        </div>
                        {isSelected && (
                          <span className="w-2 h-2 rounded-full bg-blue-600 ring-4 ring-blue-100"></span>
                        )}
                      </div>
                      <div>
                        <div className="text-xs font-bold text-gray-900 leading-tight">
                          {cat.label}
                        </div>
                        <div className="text-[11px] text-gray-500 mt-1 line-clamp-2">
                          {cat.description}
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Step 2: Department, Course & Faculty Selection (shown for academic categories or general) */}
            <div className="bg-slate-50/70 p-4 sm:p-5 rounded-2xl border border-gray-200/80 space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-gray-700 uppercase tracking-wider">
                  2. Target Department & Course{' '}
                  {!isAcademicCategory && <span className="text-gray-400 font-normal">(Optional for non-academic issues)</span>}
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-gray-600 mb-1.5">
                    Department
                  </label>
                  <select
                    value={selectedDept}
                    onChange={(e) => setSelectedDept(e.target.value)}
                    className="w-full px-3 py-2 bg-white border border-gray-300 rounded-xl text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  >
                    {departments.map((d) => (
                      <option key={d} value={d}>
                        {d}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-gray-600 mb-1.5">
                    Course {isAcademicCategory && '*'}
                  </label>
                  <select
                    value={courseId}
                    onChange={(e) => setCourseId(e.target.value)}
                    className="w-full px-3 py-2 bg-white border border-gray-300 rounded-xl text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  >
                    {!isAcademicCategory && <option value="">(None / General Campus)</option>}
                    {courses.map((c) => (
                      <option key={c.id} value={c.id}>
                        {c.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-gray-600 mb-1.5">
                    Faculty / Staff / Facility
                  </label>
                  <select
                    value={facultyId}
                    onChange={(e) => setFacultyId(e.target.value)}
                    className="w-full px-3 py-2 bg-white border border-gray-300 rounded-xl text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                  >
                    <option value="">(None / General)</option>
                    {facultyList.map((f) => (
                      <option key={f.id} value={f.id}>
                        {f.name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            {/* Step 3: Feedback Textarea */}
            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="block text-xs font-semibold text-gray-700 uppercase tracking-wider">
                  3. Feedback Details & Suggestions *
                </label>
                <span className="text-xs text-gray-400">
                  {feedbackText.length} / 2000 chars
                </span>
              </div>
              <textarea
                rows={5}
                required
                minLength={10}
                maxLength={2000}
                value={feedbackText}
                onChange={(e) => setFeedbackText(e.target.value)}
                placeholder={
                  selectedCategory === 'Canteen & Food'
                    ? "Share your feedback regarding food quality, canteen hygiene, dining cleanliness, or water facilities..."
                    : selectedCategory === 'Placements & Training'
                    ? "Share feedback regarding campus placement drives, company visits, aptitude preparation, or TPO support..."
                    : selectedCategory === 'College Services & Admin'
                    ? "Share your review regarding administrative staff, bus transport, account counter, or college office services..."
                    : selectedCategory === 'Infrastructure & Hostel'
                    ? "Share feedback regarding hostel rooms, washroom cleanliness, water supply, fans/lighting, or classroom desks..."
                    : selectedCategory === 'Library Services'
                    ? "Share feedback regarding book availability, reading room atmosphere, or library issuing procedures..."
                    : "Share your detailed constructive feedback and suggestions..."
                }
                className="w-full p-4 bg-gray-50 border border-gray-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white text-gray-900 leading-relaxed"
              />
              <p className="text-xs text-gray-400 mt-1.5 flex items-center gap-1">
                <HelpCircle className="w-3.5 h-3.5" /> NLP automatically analyzes sentiment and flags urgent issues.
              </p>
            </div>

            {/* Step 4: Anonymous Toggle */}
            <div className="p-4 bg-slate-50 border border-gray-200 rounded-xl flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-lg bg-purple-100 text-purple-700 flex items-center justify-center shrink-0">
                  <EyeOff className="w-5 h-5" />
                </div>
                <div>
                  <div className="text-sm font-semibold text-gray-900">Submit Anonymously</div>
                  <div className="text-xs text-gray-500">
                    Your identity will be protected and hidden from administrators.
                  </div>
                </div>
              </div>

              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={isAnonymous}
                  onChange={(e) => setIsAnonymous(e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
              </label>
            </div>

            {/* Submit Button */}
            <div className="flex justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => navigate('/student/dashboard')}
                className="px-5 py-2.5 border border-gray-300 text-gray-700 font-semibold rounded-xl text-sm hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={isSubmitting || feedbackText.trim().length < 10}
                className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2.5 rounded-xl shadow-md shadow-blue-500/20 text-sm transition-colors disabled:opacity-50"
              >
                {isSubmitting ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    Processing with NLP...
                  </>
                ) : (
                  <>
                    <Send className="w-4 h-4" />
                    Submit Feedback
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Real-time NLP Result Preview Modal */}
        {nlpResultModal && (
          <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
            <div className="bg-white rounded-2xl max-w-lg w-full p-6 sm:p-8 shadow-2xl border border-gray-100 animate-in fade-in zoom-in duration-200">
              <div className="flex items-center gap-3 text-emerald-600 mb-4">
                <div className="w-10 h-10 rounded-full bg-emerald-100 flex items-center justify-center">
                  <CheckCircle2 className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-gray-900">Feedback Submitted Successfully!</h3>
                  <p className="text-xs text-gray-500">Real-time NLP analysis completed</p>
                </div>
              </div>

              <div className="space-y-3 bg-slate-50 p-4 rounded-xl border border-slate-200/80 mb-6 text-xs sm:text-sm">
                <div className="flex justify-between items-center py-1.5 border-b border-gray-200/60">
                  <span className="text-gray-500 font-medium">Category:</span>
                  <span className="font-bold text-gray-900 bg-white px-2.5 py-0.5 rounded border border-gray-200">
                    {nlpResultModal.category || 'Other'}
                  </span>
                </div>

                <div className="flex justify-between items-center py-1.5 border-b border-gray-200/60">
                  <span className="text-gray-500 font-medium">Sentiment Classification:</span>
                  <span
                    className={`font-bold px-2.5 py-0.5 rounded ${
                      nlpResultModal.sentiment_label === 'Positive'
                        ? 'bg-emerald-100 text-emerald-800'
                        : nlpResultModal.sentiment_label === 'Negative'
                        ? 'bg-rose-100 text-rose-800'
                        : 'bg-amber-100 text-amber-800'
                    }`}
                  >
                    {nlpResultModal.sentiment_label} ({nlpResultModal.sentiment_score?.toFixed(2)})
                  </span>
                </div>

                <div className="flex justify-between items-center py-1.5 border-b border-gray-200/60">
                  <span className="text-gray-500 font-medium">Urgency Status:</span>
                  <span
                    className={`font-bold px-2 py-0.5 rounded ${
                      nlpResultModal.urgent
                        ? 'bg-red-100 text-red-800 border border-red-200'
                        : 'text-gray-600'
                    }`}
                  >
                    {nlpResultModal.urgent ? '🚨 Urgent Issue Detected' : 'Normal Priority'}
                  </span>
                </div>

                <div className="flex justify-between items-center py-1.5">
                  <span className="text-gray-500 font-medium">Anonymity:</span>
                  <span className="font-semibold text-gray-800">
                    {nlpResultModal.anonymous ? 'Anonymous Submission' : 'Public Submission'}
                  </span>
                </div>
              </div>

              <button
                onClick={handleCloseModal}
                className="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl text-sm transition-colors shadow-sm"
              >
                Return to Dashboard
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default FeedbackForm;
