# 💰 Smart Expense Tracker with Natural Language Processing

<div align="center">

![Version](https://img.shields.io/badge/Version-1.0.0-blue?style=flat-square&logo=github)
![Python](https://img.shields.io/badge/Python-3.8%2B-green?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square&logo=license)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Maintained](https://img.shields.io/badge/Maintained-Yes-success?style=flat-square)

**An intelligent expense tracking application that understands natural language and manages your finances effortlessly** 

✨ *No more tedious form filling. Just type like you text a friend!* ✨

✨ EXPERIENCE👇 ✨

[Smart Expense Tracker](https://smart-expense-tracker-git.streamlit.app/)
</div>

---

## 📌 Table of Contents

- [✨ Features](#-features)
- [🎯 Quick Demo](#-quick-demo)
- [🛠️ Technology Stack](#-technology-stack)
- [📋 System Architecture](#-system-architecture)
- [🚀 Getting Started](#-getting-started)
- [📖 Documentation](#-documentation)
- [🎓 Learning Resources](#-learning-resources)
- [🐛 Known Issues](#-known-issues)
- [🤝 Contributing](#-contributing)
- [📝 License](#-license)
- [👨‍💼 Author](#-author)

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎯 Core Features
- ✅ **Natural Language Input** - Type expenses like you text friends
- ✅ **Multi-Account Management** - Create unlimited accounts
- ✅ **Auto-Categorization** - AI detects spending categories
- ✅ **Smart Date Parsing** - Understands "yesterday", "5 Dec", etc.
- ✅ **Interactive Dashboards** - Beautiful charts & analytics
- ✅ **Transaction Management** - Edit, delete, filter transactions

</td>
<td width="50%">

### 🚀 Advanced Features
- 📊 **Data Visualization** - Income vs Expense, Category breakdown
- 📁 **Data Export** - Download as CSV, Excel, or PDF
- 🔐 **User Authentication** - Secure login with password hashing
- 📈 **Financial Reports** - Professional PDF reports
- 🔔 **Real-time Updates** - Instant balance calculations
- 💾 **Local Database** - All data stored securely locally

</td>
</tr>
</table>

---

## 🎯 Quick Demo

### Example Usage

**User Input:**
```
"bought milk for 50 rupees yesterday"
```

**App Understands:**
- 💵 **Amount**: ₹50.00
- 📤 **Type**: Expense
- 🏷️ **Category**: Groceries
- 📅 **Date**: Yesterday
- 📝 **Description**: milk

**App Does:**
- ✅ Saves to database
- ✅ Updates account balance
- ✅ Shows in transaction list
- ✅ Updates charts
- ✅ Generates reports

---

## 🛠️ Technology Stack

<table>
<tr>
<td align="center" width="25%">

### Frontend
![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-FF4B4B?style=for-the-badge&logo=streamlit)

</td>
<td align="center" width="25%">

### Backend
![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python)

</td>
<td align="center" width="25%">

### Database
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite)

</td>
<td align="center" width="25%">

### Hosting
![Streamlit Cloud](https://img.shields.io/badge/Streamlit%20Cloud-Deployed-09AB3B?style=for-the-badge&logo=streamlit)

</td>
</tr>
</table>

### 📚 Libraries & Tools

| Category | Technology | Version | Purpose |
|:---------|:-----------|:--------|:--------|
| 🎨 **Frontend** | Streamlit | 1.29.0 | Web App Framework |
| 📊 **Visualization** | Plotly | 5.18.0 | Interactive Charts |
| 🗣️ **NLP** | spaCy | 3.7.2 | Natural Language Processing |
| 📈 **Data Science** | Pandas | 2.1.4 | Data Manipulation |
| 📅 **Date Parsing** | python-dateutil | 2.8.2 | Flexible Date Handling |
| 📄 **PDF Export** | ReportLab | 4.0.7 | PDF Generation |
| 📊 **Excel Export** | openpyxl | 3.1.2 | Excel Support |
| 🔐 **Security** | bcrypt | Latest | Password Hashing |

---

## 📋 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 PRESENTATION LAYER                      │
│           (Streamlit Web Interface)                      │
│  - Account Management    - Transaction Forms             │
│  - Dashboard             - Charts & Reports              │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ├─────────────────────────────┐
                  │                             │
        ┌─────────▼──────────┐        ┌────────▼─────────┐
        │ APPLICATION LAYER  │        │  VISUALIZATION   │
        ├────────────────────┤        ├──────────────────┤
        │ • NLP Parser       │        │ • Plotly Charts  │
        │ • Data Processor   │        │ • PDF Generator  │
        │ • Business Logic   │        │ • Report Builder │
        └─────────┬──────────┘        └─────────────────┘
                  │
        ┌─────────▼──────────────┐
        │   DATA ACCESS LAYER    │
        ├───────────────────────┤
        │  DatabaseManager      │
        │  • CRUD Operations    │
        │  • Query Builder      │
        │  • Transaction Mgmt   │
        └─────────┬─────────────┘
                  │
        ┌─────────▼──────────────┐
        │  PERSISTENCE LAYER     │
        ├───────────────────────┤
        │  SQLite Database      │
        │  • Accounts Table     │
        │  • Transactions Table │
        │  • Indexes & Queries  │
        └───────────────────────┘
```

---

## 🚀 Getting Started

### 📥 Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8** or higher
- **pip** (Python package manager)
- **Git** (for version control)
- **4 GB RAM** minimum (8 GB recommended)

### 💻 Installation

#### Step 1️⃣: Clone the Repository
```bash
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker
```

#### Step 2️⃣: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Step 3️⃣: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4️⃣: Download spaCy Language Model
```bash
python -m spacy download en_core_web_sm
```

#### Step 5️⃣: Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501` 🎉

---

## 📖 How to Use

### 1️⃣ **Create an Account**
```
Click "Create New Account" in the sidebar
Enter account name (e.g., "Home", "School")
Optional: Add description
Click "Create"
```

### 2️⃣ **Add a Transaction**
```
Type in the text area:
"bought milk for 50 rupees yesterday"

Click "Parse & Add"

The app will automatically:
✓ Extract amount
✓ Detect type (income/expense)
✓ Categorize
✓ Set date
✓ Save to database
```

### 3️⃣ **View Transactions**
```
All transactions shown in table
Filter by date range
Sort by amount, category, type
Edit or delete as needed
```

### 4️⃣ **Generate Reports**
```
Select date range
Choose account
Click "Generate PDF"
Download and share
```

### 📝 Supported Input Formats

```
✓ "bought pen for 5 rupees"
✓ "spent 50 on milk on Dec 5"
✓ "got 2000 rupees salary"
✓ "paid 200 yesterday"
✓ "₹500 on groceries"
✓ "Rs. 100 for transport"
✓ "spent 50 today"
✓ "added 1000 yesterday"
```

---

## 📁 Project Structure

```
expense-tracker/
│
├── 📄 app.py                          # Main Streamlit application
├── ⚙️ config.py                       # Configuration settings
├── 📋 requirements.txt                # Python dependencies
├── 📖 README.md                       # Project documentation
├── 🔑 .gitignore                      # Git ignore rules
│
├── 📂 database/
│   ├── 🐍 __init__.py
│   ├── 🗄️ schema.sql                 # Database schema
│   └── 🔧 db_manager.py              # Database operations
│
├── 📂 nlp/
│   ├── 🐍 __init__.py
│   ├── 🎯 parser.py                  # NLP parsing logic
│   └── 📋 patterns.py                # Regex patterns
│
├── 📂 utils/
│   ├── 🐍 __init__.py
│   ├── 📊 data_processor.py          # Data analysis
│   ├── 📈 visualizations.py          # Chart generation
│   ├── 📄 pdf_generator.py           # PDF creation
│   └── 🛠️ helpers.py                 # Utilities
│
├── 📂 data/
│   └── 💾 expenses.db                # SQLite database
│
├── 📂 tests/
│   ├── 🐍 __init__.py
│   ├── ✅ test_database.py           # DB tests
│   ├── ✅ test_parser.py             # NLP tests
│   └── ✅ test_integration.py        # Integration tests
│
├── 📂 docs/
│   ├── 📚 CONTRIBUTING.md            # Contribution guidelines
│   ├── 📖 API_DOCUMENTATION.md       # API docs
│   └── 🚀 DEPLOYMENT_GUIDE.md        # Deployment steps
│
└── 📂 assets/
    ├── 🖼️ screenshots/               # App screenshots
    └── 📊 sample_data/               # Test datasets
```

---

## 🎓 Learning Resources

This project includes comprehensive documentation for learning:

### 📚 Main Documents
- **[Comprehensive Project Report](./docs/Expense_Tracker_Report.md)** - 15,000+ words with code examples
- **[Beginner's Learning Guide](./docs/Learning_Guide.md)** - Step-by-step learning path
- **[API Documentation](./docs/API_DOCUMENTATION.md)** - Complete code reference

### 🎯 Topics Covered
- ✅ Database design & SQL optimization
- ✅ Natural Language Processing with regex & spaCy
- ✅ Python OOP & design patterns
- ✅ Web development with Streamlit
- ✅ Data visualization with Plotly
- ✅ PDF report generation
- ✅ User authentication & security
- ✅ Cloud deployment

### 🔗 External Resources
- [Streamlit Documentation](https://docs.streamlit.io/)
- [spaCy NLP Guide](https://spacy.io/usage)
- [SQLite Tutorial](https://www.sqlite.org/tutorial.html)
- [Plotly Charts](https://plotly.com/python/)
- [Regular Expressions](https://regex101.com/)

---

## 📊 Key Statistics

| Metric | Value |
|:------:|:-----:|
| 📝 **Lines of Code** | 2,000+ |
| 📦 **Python Modules** | 8 |
| 🗄️ **Database Tables** | 2 |
| 📊 **Chart Types** | 3 |
| ⏱️ **Development Time** | 40+ hours |
| 🧪 **Test Coverage** | 85%+ |
| 📚 **Documentation Pages** | 5 |

---

## 🎨 Screenshots & Demo

### 📱 Main Dashboard
```
┌─────────────────────────────────────────────────┐
│  💰 Smart Expense Tracker                        │
├─────────────────────────────────────────────────┤
│                                                   │
│  Select Account: [Home ▼]                        │
│                                                   │
│  ┌──────────────────────────────────────────┐   │
│  │  📊 Current Balance: ₹4,650              │   │
│  │  💵 Total Income: ₹5,000                 │   │
│  │  📉 Total Expenses: ₹350                 │   │
│  └──────────────────────────────────────────┘   │
│                                                   │
│  Add Transaction:                                │
│  ┌──────────────────────────────────────────┐   │
│  │ bought milk for 50 rupees               │   │
│  └──────────────────────────────────────────┘   │
│  [Parse & Add] [Manual Entry]                    │
│                                                   │
└─────────────────────────────────────────────────┘
```

### 📈 Analytics Dashboard
```
Income vs Expenses          Category Breakdown
┌──────────────────┐       ┌──────────────────┐
│  ▄▄▄             │       │    Groceries     │
│  ▄▄▄  ▃▃▃        │       │   /  \           │
│  ▄▄▄  ▃▃▃        │       │  /    \          │
│ Income Expense   │       │ 45%    55%       │
└──────────────────┘       └──────────────────┘

Spending Trend Over Time
┌───────────────────────────────────────┐
│  ╱╲        ╱╲                         │
│ ╱  ╲  ╱╲  ╱  ╲                        │
│╱    ╲╱  ╲╱    ╲                       │
│  Dec 1  Dec 7   Dec 15                │
└───────────────────────────────────────┘
```

---

## 🔧 Configuration

### 🎨 Customize Appearance
Edit `config.py`:
```python
# App Settings
APP_NAME = "💰 Smart Expense Tracker"
APP_ICON = "💰"

# Theme
PRIMARY_COLOR = "#FF6B9D"
SECONDARY_COLOR = "#F0F2F6"

# Database
DB_PATH = "data/expenses.db"
```

### 🏷️ Add Custom Categories
Edit `nlp/patterns.py`:
```python
CATEGORY_KEYWORDS = {
    "Groceries": ["milk", "vegetables", "fruits"],
    "Health": ["medicine", "doctor", "hospital"],
    "Entertainment": ["movie", "game", "netflix"],
    # Add more as needed
}
```

---

## 🚀 Deployment

### ☁️ Deploy to Streamlit Cloud (Recommended)

**Step 1:** Push to GitHub
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

**Step 2:** Create Streamlit Cloud Account
- Visit [share.streamlit.io](https://share.streamlit.io)
- Sign up with GitHub account

**Step 3:** Deploy
- Click "New app"
- Select repository
- Set main file to `app.py`
- Click "Deploy"

**Your app is live!** 🎉
```
https://share.streamlit.io/yourusername/expense-tracker/app.py
```

### 📦 Alternative Deployment Options

| Platform | Cost | Ease | Speed |
|:---------|:----:|:----:|:-----:|
| **Streamlit Cloud** | Free | ⭐⭐⭐⭐⭐ | Fast |
| **Heroku** | Free/Paid | ⭐⭐⭐⭐ | Medium |
| **AWS/Azure** | Paid | ⭐⭐⭐ | Varies |
| **PythonAnywhere** | Free/Paid | ⭐⭐⭐⭐ | Fast |

---

## 🐛 Known Issues

| Issue | Status | Workaround |
|:------|:------:|:-----------|
| spaCy download fails on Windows | ⚠️ Fixed | Use wheel file directly |
| PowerShell execution policy blocks venv activation | ⚠️ Fixed | Use Command Prompt or PowerShell as Admin |
| Large PDF generation slow | ⏳ Investigating | Optimize for reports <1000 transactions |
| Date parsing ambiguous (5/12/2025) | ✅ Solved | Uses dayfirst=True for Indian format |

---

## 💡 Troubleshooting

### Issue: ModuleNotFoundError
**Solution:**
```bash
# Ensure virtual environment is activated
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Issue: Database locked
**Solution:**
```bash
# Close all app instances and restart
rm data/expenses.db  # Backup first!
streamlit run app.py
```

### Issue: spaCy model not found
**Solution:**
```bash
# Download language model
python -m spacy download en_core_web_sm
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to help:

### 🎯 Ways to Contribute

1. **🐛 Report Bugs** - Found an issue? Open a GitHub issue
2. **💡 Suggest Features** - Have an idea? Discuss in discussions tab
3. **📝 Documentation** - Improve docs and examples
4. **🔧 Code Improvements** - Submit pull requests
5. **🧪 Add Tests** - Increase code coverage
6. **🌍 Translate** - Support new languages

### 📋 Learning Guidelines

Please see [Learning_Guide.md](./Learning_Guide.md) for detailed learning guidelines.

**Quick Steps:**
1. Fork the repository
2. Create a branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📋 Testing

### Run Unit Tests
```bash
pytest tests/test_database.py -v
pytest tests/test_parser.py -v
pytest tests/test_integration.py -v
```

### Run All Tests
```bash
pytest tests/ --cov=. --cov-report=html
```

### Test Coverage
Current coverage: **85%+**

---

## 📝 License

This project is licensed under the **MIT License** - see [LICENSE](./LICENSE) file for details.

### What You Can Do ✅
- ✅ Use for personal projects
- ✅ Modify the code
- ✅ Distribute copies
- ✅ Use in commercial projects

### What You Must Do ⚠️
- ⚠️ Include license notice
- ⚠️ State changes made

---

<!--## 📞 Support & Community

### 💬 Get Help

| Channel | Link | Response Time |
|:--------|:----:|:--------------:|
| **GitHub Issues** | [Open Issue](https://github.com/yourusername/expense-tracker/issues) | 24-48 hours |
| **Discussions** | [Join Discussion](https://github.com/yourusername/expense-tracker/discussions) | 48-72 hours |
| **Email** | yourname@email.com | 24-48 hours |-->

### 🌟 Show Your Support

⭐ **Star** this repository if you found it helpful!

🔗 **Share** with your network

💬 **Feedback** is appreciated

---

## 🎓 Learning Outcomes

After completing this project, you'll understand:

- ✅ **Database Design** - Schema, relationships, optimization
- ✅ **NLP Fundamentals** - Regex, entity extraction, intent detection
- ✅ **Web Development** - Streamlit, interactive UIs, real-time updates
- ✅ **Data Science** - Pandas, aggregation, visualization
- ✅ **Security** - Password hashing, session management, SQL injection prevention
- ✅ **Deployment** - Cloud hosting, Git workflows, CI/CD concepts

---

## 🚀 Roadmap

### v1.1.0 (Planned)
- [ ] Dark mode theme
- [ ] Recurring transactions
- [ ] Budget alerts
- [ ] Multi-currency support
- [ ] Export to Excel with formatting

### v1.2.0 (Future)
- [ ] Mobile app (React Native)
- [ ] Machine learning categorization
- [ ] Voice input support
- [ ] Family/group accounts
- [ ] Bank API integration

### v2.0.0 (Long-term)
- [ ] Web version with authentication
- [ ] Cloud database (PostgreSQL)
- [ ] Advanced analytics & forecasting
- [ ] API for third-party integrations
- [ ] Plugin system

---

## 👨‍💼 Author

**Satyam Dubey**
- 📧 Email: satyamdubey2988@gmail.com
- 🔗 GitHub: [dubeysatyam2002](https://github.com/dubeysatyam2002)
- 💼 LinkedIn: [Satyam Dubey](https://www.linkedin.com/in/satyam-dubey-8698b81b7/)
<!--- 🌐 Portfolio: [Your Website](https://yourwebsite.com)-->

### 🙏 Acknowledgments

- 🙏 Thanks to ChatGPT for guidance and learning support
- 🙏 Streamlit community for amazing framework
- 🙏 spaCy team for NLP library
- 🙏 All contributors and supporters

---

## 📊 Project Stats

![GitHub Stars](https://img.shields.io/github/stars/dubeysatyam2002/expense-tracker?style=social)
![GitHub Forks](https://img.shields.io/github/forks/dubeysatyam2002/expense-tracker?style=social)
![GitHub Issues](https://img.shields.io/github/issues/dubeysatyam2002/expense-tracker)
![GitHub Pull Requests](https://img.shields.io/github/issues-pr/dubeysatyam2002/expense-tracker)

---

## 🔒 Security

This project prioritizes security:
- ✅ Passwords hashed with bcrypt (not plaintext)
- ✅ SQL injection prevention (parameterized queries)
- ✅ Session-based authentication
- ✅ Data stored locally (no external servers)
- ✅ ACID compliance with SQLite

### 🛡️ Security Policy

If you discover a security vulnerability, please email `satyamdubey2988@gmail.com` instead of using the issue tracker.

---

## 📮 Contact & Feedback

Have questions or suggestions? I'd love to hear from you!

- 📨 **Email:** satyamdubey2988@gmail.com
- 💬 **GitHub Discussions:** [Start a discussion](https://github.com/dubeysatyam2002/expense-tracker/discussions)
- 🐛 **Report Issues:** [Open an issue](https://github.com/dubeysatyam2002/expense-tracker/issues)
- ⭐ **Leave feedback:** Star this repo and share your thoughts!

---

<div align="center">

### Made by [Satyam Dubey]

**[⬆ Back to top](#-smart-expense-tracker-with-natural-language-processing)**

![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)
![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)
![forthebadge](https://forthebadge.com/images/badges/open-source.svg)

---

**Don't forget to:**
- ⭐ Star this repository
- 🔄 Follow for updates
- 📤 Share with your network

Happy Learning! 💰✨

</div>
