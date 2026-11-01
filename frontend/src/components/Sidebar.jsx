import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  LayoutDashboard,
  PlusCircle,
  History,
  BarChart3,
  TableProperties,
  AlertTriangle,
  Lightbulb,
} from 'lucide-react';

const Sidebar = () => {
  const { isStudent, isAdmin } = useAuth();

  const studentLinks = [
    {
      to: '/student/dashboard',
      label: 'Student Dashboard',
      icon: LayoutDashboard,
    },
    {
      to: '/student/feedback/new',
      label: 'Submit Feedback',
      icon: PlusCircle,
    },
    {
      to: '/student/history',
      label: 'My Feedback History',
      icon: History,
    },
  ];

  const adminLinks = [
    {
      to: '/admin/dashboard',
      label: 'Analytics Dashboard',
      icon: BarChart3,
    },
    {
      to: '/admin/feedback',
      label: 'Feedback Management',
      icon: TableProperties,
    },
  ];

  const links = isAdmin ? adminLinks : studentLinks;

  return (
    <aside className="w-full md:w-64 bg-white border-r border-gray-200 md:min-h-[calc(100vh-4rem)] p-4 flex flex-col justify-between shrink-0">
      <div>
        <div className="text-[11px] uppercase tracking-wider font-bold text-gray-400 px-3 mb-2">
          {isAdmin ? 'Administration Portal' : 'Student Portal'}
        </div>
        <nav className="space-y-1">
          {links.map((link) => {
            const Icon = link.icon;
            return (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-blue-50 text-blue-700 font-semibold border border-blue-100 shadow-xs'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100/80'
                  }`
                }
              >
                <Icon className="w-4 h-4 shrink-0" />
                {link.label}
              </NavLink>
            );
          })}
        </nav>
      </div>

      {/* Helpful viva guide / info card in sidebar footer */}
      <div className="mt-6 pt-4 border-t border-gray-100">
        <div className="bg-gradient-to-br from-slate-50 to-blue-50/50 p-3.5 rounded-xl border border-blue-100/60">
          <div className="flex items-center gap-2 text-xs font-semibold text-blue-900 mb-1">
            <Lightbulb className="w-3.5 h-3.5 text-blue-600 shrink-0" />
            AI Pipeline Active
          </div>
          <p className="text-[11px] text-gray-600 leading-relaxed">
            Every submission is preprocessed, evaluated with VADER sentiment, categorized, and checked for urgency.
          </p>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
