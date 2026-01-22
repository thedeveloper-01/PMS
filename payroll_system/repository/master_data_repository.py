"""
Master data repository for database operations
"""
from typing import List, Optional
from payroll_system.models.master_data import Department, Designation, Branch, Shift, Holiday
from payroll_system.utils.database import db
import logging

logger = logging.getLogger(__name__)

class MasterDataRepository:
    """Repository for master data operations"""
    
    def __init__(self):
        self.departments = db.get_db().departments
        self.designations = db.get_db().designations
        self.branches = db.get_db().branches
        self.shifts = db.get_db().shifts
        self.holidays = db.get_db().holidays
    
    # Department operations
    def create_department(self, department: Department) -> bool:
        try:
            result = self.departments.insert_one(department.to_dict())
            return result.inserted_id is not None
        except Exception as e:
            logger.error(f"Error creating department: {e}")
            return False
    
    def get_department(self, department_id: str) -> Optional[Department]:
        try:
            data = self.departments.find_one({'department_id': department_id})
            if data:
                return Department(
                    department_id=data['department_id'],
                    department_name=data['department_name'],
                    created_date=data.get('created_date'),
                    modified_date=data.get('modified_date'),
                    status=data.get('status', 1)
                )
            return None
        except Exception as e:
            logger.error(f"Error getting department: {e}")
            return None

    def get_all_departments(self) -> List[Department]:
        try:
            departments = []
            for data in self.departments.find({'status': 1}):
                departments.append(Department(
                    department_id=data['department_id'],
                    department_name=data['department_name'],
                    created_date=data.get('created_date'),
                    modified_date=data.get('modified_date'),
                    status=data.get('status', 1)
                ))
            return departments
        except Exception as e:
            logger.error(f"Error getting departments: {e}")
            return []
    
    # Designation operations
    def create_designation(self, designation: Designation) -> bool:
        try:
            result = self.designations.insert_one(designation.to_dict())
            return result.inserted_id is not None
        except Exception as e:
            logger.error(f"Error creating designation: {e}")
            return False
    
    def get_designation(self, designation_id: str) -> Optional[Designation]:
        try:
            data = self.designations.find_one({'designation_id': designation_id})
            if data:
                return Designation(
                    designation_id=data['designation_id'],
                    designation_name=data['designation_name'],
                    department_name=data['department_name'],
                    created_date=data.get('created_date'),
                    modified_date=data.get('modified_date'),
                    status=data.get('status', 1)
                )
            return None
        except Exception as e:
            logger.error(f"Error getting designation: {e}")
            return None

    def get_all_designations(self) -> List[Designation]:
        try:
            designations = []
            for data in self.designations.find({'status': 1}):
                designations.append(Designation(
                    designation_id=data['designation_id'],
                    designation_name=data['designation_name'],
                    department_name=data['department_name'],
                    created_date=data.get('created_date'),
                    modified_date=data.get('modified_date'),
                    status=data.get('status', 1)
                ))
            return designations
        except Exception as e:
            logger.error(f"Error getting designations: {e}")
            return []
    
    # Branch operations
    def create_branch(self, branch: Branch) -> bool:
        try:
            result = self.branches.insert_one(branch.to_dict())
            return result.inserted_id is not None
        except Exception as e:
            logger.error(f"Error creating branch: {e}")
            return False
    
    def get_all_branches(self) -> List[Branch]:
        try:
            branches = []
            for data in self.branches.find({'status': 1}):
                branches.append(Branch(
                    branch_id=data['branch_id'],
                    name=data['name'],
                    branch_address=data['branch_address'],
                    phone_number=data['phone_number'],
                    email=data['email'],
                    establishment_date=data.get('establishment_date'),
                    created_by=data.get('created_by', ''),
                    created_date=data.get('created_date'),
                    modified_date=data.get('modified_date'),
                    status=data.get('status', 1)
                ))
            return branches
        except Exception as e:
            logger.error(f"Error getting branches: {e}")
            return []
    
    # Shift operations
    def create_shift(self, shift: Shift) -> bool:
        try:
            result = self.shifts.insert_one(shift.to_dict())
            return result.inserted_id is not None
        except Exception as e:
            logger.error(f"Error creating shift: {e}")
            return False
    
    def get_all_shifts(self) -> List[Shift]:
        try:
            shifts = []
            for data in self.shifts.find({'status': 1}):
                shifts.append(Shift(
                    shift_id=data['shift_id'],
                    shift_name=data['shift_name'],
                    in_time=data['in_time'],
                    out_time=data['out_time'],
                    created_date=data.get('created_date'),
                    modified_date=data.get('modified_date'),
                    status=data.get('status', 1)
                ))
            return shifts
        except Exception as e:
            logger.error(f"Error getting shifts: {e}")
            return []
    
    # Holiday operations
    def create_holiday(self, holiday: Holiday) -> bool:
        try:
            result = self.holidays.insert_one(holiday.to_dict())
            return result.inserted_id is not None
        except Exception as e:
            logger.error(f"Error creating holiday: {e}")
            return False
    
    def get_all_holidays(self) -> List[Holiday]:
        try:
            holidays = []
            for data in self.holidays.find({'status': 1}):
                from datetime import datetime as dt
                holiday_date = None
                if data.get('holiday_date'):
                    if isinstance(data['holiday_date'], str):
                        holiday_date = dt.strptime(data['holiday_date'], '%Y-%m-%d').date()
                    else:
                        holiday_date = data['holiday_date']
                
                holidays.append(Holiday(
                    holiday_id=data['holiday_id'],
                    holiday_name=data['holiday_name'],
                    holiday_date=holiday_date,
                    holiday_description=data.get('holiday_description', ''),
                    created_date=data.get('created_date'),
                    modified_date=data.get('modified_date'),
                    status=data.get('status', 1)
                ))
            return holidays
        except Exception as e:
            logger.error(f"Error getting holidays: {e}")
            return []

    # Delete operations
    def delete_department(self, department_id: str) -> bool:
        try:
            result = self.departments.update_one(
                {'department_id': department_id},
                {'$set': {'status': 0}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error deleting department: {e}")
            return False

    def delete_designation(self, designation_id: str) -> bool:
        try:
            result = self.designations.update_one(
                {'designation_id': designation_id},
                {'$set': {'status': 0}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error deleting designation: {e}")
            return False

    def delete_branch(self, branch_id: str) -> bool:
        try:
            result = self.branches.update_one(
                {'branch_id': branch_id},
                {'$set': {'status': 0}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error deleting branch: {e}")
            return False

    def delete_shift(self, shift_id: str) -> bool:
        try:
            result = self.shifts.update_one(
                {'shift_id': shift_id},
                {'$set': {'status': 0}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error deleting shift: {e}")
            return False

    def delete_holiday(self, holiday_id: str) -> bool:
        try:
            result = self.holidays.update_one(
                {'holiday_id': holiday_id},
                {'$set': {'status': 0}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error deleting holiday: {e}")
            return False

