<img width="1358" height="715" alt="Reports" src="https://github.com/user-attachments/assets/2d1d95c4-764f-4cf8-8c17-fd390323bc8c" />
# SDFMS - Smart Department Finance Management System

SDFMS (Smart Department Finance Management System) is a standalone desktop application designed specifically for university departments to manage their financial operations. It provides a complete solution for tracking student payments, managing funds and campaigns, generating receipts, and producing comprehensive financial reports.

### **Key Features**

- 📊 **Dashboard** - Real-time financial overview with statistics and quick actions
- 👨‍🎓 **Student Management** - Register, search, and manage students with custom roll numbers
- 💰 **Fund Management** - Create and manage unlimited funds with types
- 📋 **Campaign Management** - Create collection campaigns targeting specific student groups
- 💳 **Payment Collection** - Collect payments with auto-generated receipts (PDF + QR)
- 📤 **Expense Management** - Track department expenses with receipt upload
- 📈 **Reports & Analytics** - 10+ comprehensive charts and exportable reports (PDF/Excel)
- ⚙️ **Settings** - Configure department, academic structure, and receipt settings




## **Screenshots**

| Dashboard | Payment Collection |
|-----------|-------------------|
| ---<img width="1363" height="727" alt="Dashboard" src="https://github.com/user-attachments/assets/b8a7253e-eaac-46e8-9353-ec2d242d5d4b" />| <img width="1363" height="718" alt="Payment" src="https://github.com/user-attachments/assets/af50f463-6f8d-4b80-ad6c-405d19e0d7f3" /> |

| Reports | Charts |

|---------|--------|
| <img width="1358" height="715" alt="Reports" src="https://github.com/user-attachments/assets/68d67fd3-6dde-43f2-ae3a-7d2950681c85" />| <img width="1366" height="722" alt="Charts" src="https://github.com/user-attachments/assets/e86b4b7b-eb8e-4a87-a160-9c194f39403c" /> |

---

## **Quick Start**

### Download

1. Download the latest release from [Releases](https://github.com/yourusername/sdfms/releases)
2. Extract the ZIP file
3. Run `SDFMS.exe`

### First Run Setup

1. **First Run Wizard** appears automatically
2. Fill in your department details:
   - University Name (e.g., GC University Faisalabad)
   - Department Name (e.g., Computer Science)
   - Department Code (e.g., CS)
   - Receipt Prefix (e.g., CS)
3. Click **"Launch"**

### Post-Setup Steps

1. **Set up Academic Structure** (`Settings → Academics`)
   - Add Sessions: 2022, 2023, 2024...
   - Add Programs: BSCS, BSSE, BSIT...
   - Add Shifts: Morning, Evening
   - Add Sections: A, B, C, D

2. **Register Students** (`Students → Add Student`)

3. **Create Funds** (`Funds → Add Fund`)

4. **Create Campaigns** (`Campaigns → Add Campaign`)

5. **Start Collecting Payments** (`Payments → Collect Payment`)

---

##  **System Requirements**

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | Windows 7 (64-bit) | Windows 10/11 (64-bit) |
| **Processor** | Intel Core i3 | Intel Core i5 |
| **RAM** | 2 GB | 4 GB |
| **Storage** | 200 MB | 500 MB |
| **Resolution** | 1024 x 768 | 1366 x 768+ |
| **.NET Framework** | 4.5+ | 4.8+ |

---

## **Folder Structure**

SDFMS/
├── SDFMS.exe # Main executable
├── data/
│ ├── database/
│ │ └── dffms.db # SQLite database
│ ├── receipts/ # Generated receipts (PDF + QR)
│ ├── exports/ # Exported reports (PDF/Excel)
│ ├── backups/ # Database backups
│ └── logs/ # Application logs
└── src/ # (Embedded in EXE)



---

## 🛠️ **Development Setup**

If you want to run from source or contribute:

### Prerequisites

- Python 3.12 or higher
- Git

### Clone & Install

```bash
# Clone the repository
git clone https://github.com/yourusername/sdfms.git
cd sdfms

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py


🎯 Features in Detail

📊 Dashboard

Welcome header with date/time
Quick action buttons (Collect Payment, Add Student, etc.)
6 statistics cards with progress indicators
Recent activity feed

Today's summary

👨‍🎓 Student Management
Manual roll number entry (format: PROGRAM-SESSION-001)
Filter by Session, Semester, Program
Search by name or roll number
Quick payment from student list


 Fund Management

Create unlimited funds with types
Fund types: General, Academic, Event, Tour, Lab, Sports, Workshop, Industrial Visit, Farewell, Other
Activate/Deactivate funds
Delete funds (only if no campaigns linked)


 Campaign Management

Target specific student groups (Program, Session, Semester, Shift)
Auto-track paid/pending students
Collection percentage display
Campaign details with paid/pending lists

 Payment Collection

Search student by roll number
Show only eligible (unpaid) campaigns
Auto-fill required amount
Receipt generation (PDF + QR code)
Receipt popup preview
Payment history with filters

📤 Expense Management

Add expenses with fund selection
Receipt image upload
Filter by fund
Total expenses calculation

 Reports

Collection Report (with date filters)
Expense Report (with date filters)
Fund Performance (Profitable/Loss/Break-even)
10 Comprehensive Charts:

Semester-wise Collection
Collection vs Expenses by Fund
Collection Distribution by Fund
Fund Performance (Balance)
Student Payment Status
Campaign Performance
Expense Breakdown by Fund
Daily Collection (Last 7 Days)
Monthly Collection Trend
Fund Health Status


 Settings

General Settings (Department/University info)
Academic Structure (Sessions, Programs, Shifts, Sections)
Receipt Settings (Prefix)
Backup & Restore



 Database Schema

The application uses SQLite with the following main tables:
departments - Department settings
sessions, programs, shifts, sections - Academic structure
students - Student records
funds - Fund management
campaigns - Collection campaigns
payments - Payment records
expenses - Expense records


Support

 Email: usmanumardraz56@gmail.com
 Phone: +92-3074825440


 Acknowledgments

Built with CustomTkinter
PDF generation with ReportLab
Charts with Matplotlib
QR codes with qrcode

 Developed For
Developed as a Semester Project for Department of Computer Science, GC University Faisalabad.

Made with ❤️ by Usman
Department of Computer Science
GC University Faisalabad
