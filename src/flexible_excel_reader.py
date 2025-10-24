"""
Flexibel Excel Reader för LIA-rapporter
Anpassar sig automatiskt till olika Excel-format med liknande struktur
"""

import pandas as pd
from typing import Dict, List, Optional, Tuple
import logging
import re

# Konfigurera logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FlexibleLIAExcelReader:
    """Flexibel klass för att läsa olika format av LIA-rapporter från Excel"""
    
    def __init__(self, file_path: str):
        """
        Initialiserar Excel-läsaren
        
        Args:
            file_path (str): Sökväg till Excel-filen
        """
        self.file_path = file_path
        self.df = None
        self.students_data = []
        self.column_mapping = {}
        self.assessment_areas = []
        
    def load_excel(self) -> bool:
        """
        Laddar Excel-filen
        
        Returns:
            bool: True om fil laddades framgångsrikt, False annars
        """
        try:
            logger.info(f"Laddar Excel-fil: {self.file_path}")
            self.df = pd.read_excel(self.file_path)
            logger.info(f"Fil laddad framgångsrikt. Antal rader: {len(self.df)}")
            return True
        except Exception as e:
            logger.error(f"Fel vid laddning av Excel-fil: {e}")
            return False
    
    def auto_detect_structure(self) -> bool:
        """
        Analyserar Excel-strukturen automatiskt och mappar kolumner
        
        Returns:
            bool: True om strukturen kunde identifieras, False annars
        """
        if self.df is None:
            logger.error("Excel-fil inte laddad")
            return False
        
        try:
            logger.info("🔍 Analyserar Excel-struktur automatiskt...")
            
            # Identifiera grundläggande kolumner
            self._identify_basic_columns()
            
            # Identifiera bedömningsområden
            self._identify_assessment_areas()
            
            # Identifiera slutbetyg och kommentarer
            self._identify_final_sections()
            
            logger.info(f"✅ Struktur identifierad: {len(self.assessment_areas)} bedömningsområden")
            return True
            
        except Exception as e:
            logger.error(f"Fel vid strukturanalys: {e}")
            return False
    
    def _identify_basic_columns(self):
        """Identifierar grundläggande kolumner (namn, företag, handledare, etc.)"""
        
        # Studentnamn
        name_patterns = ['namn.*studerande', 'student.*namn', 'namn.*student', r'q\d+.*namn.*studerande']
        self.column_mapping['student_name'] = self._find_column_by_patterns(name_patterns)
        
        # Företag
        company_patterns = ['namn.*företag', 'företag.*namn', r'q\d+.*företag']
        self.column_mapping['company'] = self._find_column_by_patterns(company_patterns)
        
        # Handledare
        supervisor_patterns = ['namn.*handledare', 'handledare.*namn', r'q\d+.*handledare']
        self.column_mapping['supervisor'] = self._find_column_by_patterns(supervisor_patterns)
        
        # Närvarotid
        attendance_patterns = ['närvarotimmar', 'närvaro.*tid', r'q\d+.*närvarotimmar', r'q\d+.*företaget']
        self.column_mapping['attendance'] = self._find_column_by_patterns(attendance_patterns)
        
        logger.info(f"Grundkolumner identifierade: {self.column_mapping}")
    
    def _find_column_by_patterns(self, patterns: List[str]) -> Optional[str]:
        """
        Hittar kolumn som matchar något av mönstren
        
        Args:
            patterns: Lista med regex-mönster att söka efter
            
        Returns:
            Kolumnnamn eller None om ingen hittas
        """
        for column in self.df.columns:
            column_lower = column.lower()
            for pattern in patterns:
                if re.search(pattern, column_lower):
                    return column
        return None
    
    def _identify_assessment_areas(self):
        """Identifierar bedömningsområden och kommentarer"""
        self.assessment_areas = []
        
        # Hitta alla Q-frågor som inte är grundinfo
        q_columns = [col for col in self.df.columns if col.startswith('Q')]
        
        # Sorterar efter Q-nummer
        q_columns.sort(key=lambda x: int(x.split(':')[0][1:]) if ':' in x else 999)
        
        # Identifiera bedömningsområden (inte grundinfo, inte slutbetyg/kommentarer)
        skip_patterns = [
            'namn.*studerande', 'namn.*företag', 'namn.*handledare', 
            'närvarotimmar', 'helhetsintryck', 'kommentarer$', 'kommentar$'
        ]
        
        i = 0
        while i < len(q_columns):
            current_col = q_columns[i]
            current_lower = current_col.lower()
            
            # Skippa grundinfo och slutsektioner
            if any(re.search(pattern, current_lower) for pattern in skip_patterns):
                i += 1
                continue
            
            # Kolla om detta är en kommentarskolumn
            if 'kommentar' in current_lower and not current_lower.endswith('kommentarer'):
                i += 1
                continue
            
            # Detta borde vara ett bedömningsområde
            assessment = {
                'question_column': current_col,
                'comment_column': None
            }
            
            # Leta efter tillhörande kommentarskolumn
            if i + 1 < len(q_columns):
                next_col = q_columns[i + 1]
                if 'kommentar' in next_col.lower() and not next_col.lower().endswith('kommentarer'):
                    assessment['comment_column'] = next_col
                    i += 1  # Hoppa över kommentarskolumnen
            
            self.assessment_areas.append(assessment)
            i += 1
        
        logger.info(f"Identifierade {len(self.assessment_areas)} bedömningsområden")
    
    def _identify_final_sections(self):
        """Identifierar slutbetyg och kommentarer"""
        
        # Helhetsintryck/slutbetyg
        final_patterns = ['helhetsintryck', 'slutbetyg', 'total.*betyg', 'övergripande']
        self.column_mapping['final_grade'] = self._find_column_by_patterns(final_patterns)
        
        # Slutkommentarer
        comment_patterns = ['kommentarer$', 'slutkommentar', 'avslutande.*kommentar']
        self.column_mapping['final_comments'] = self._find_column_by_patterns(comment_patterns)
        
        logger.info(f"Slutsektioner: Betyg='{self.column_mapping['final_grade']}', Kommentarer='{self.column_mapping['final_comments']}'")
    
    def extract_student_data(self) -> bool:
        """
        Extraherar data för alla studenter
        
        Returns:
            bool: True om data extraherades framgångsrikt
        """
        if self.df is None or not self.column_mapping:
            logger.error("Excel-fil inte laddad eller struktur inte analyserad")
            return False
        
        try:
            self.students_data = []
            
            for index, row in self.df.iterrows():
                student_data = self._extract_single_student(row)
                if student_data:
                    self.students_data.append(student_data)
                    logger.info(f"Student extraherad: {student_data.get('student_name', f'Student {index+1}')}")
            
            logger.info(f"Totalt {len(self.students_data)} studenter extraherade")
            return True
            
        except Exception as e:
            logger.error(f"Fel vid extraktion av studentdata: {e}")
            return False
    
    def _extract_single_student(self, row) -> Optional[Dict]:
        """Extraherar data för en enskild student"""
        try:
            # Grundläggande info
            student_data = {
                'student_name': self._get_cell_value(row, self.column_mapping.get('student_name')),
                'company': self._get_cell_value(row, self.column_mapping.get('company')),
                'supervisor': self._get_cell_value(row, self.column_mapping.get('supervisor')),
                'attendance': self._get_cell_value(row, self.column_mapping.get('attendance')),
                'final_grade': self._get_cell_value(row, self.column_mapping.get('final_grade')),
                'final_comments': self._get_cell_value(row, self.column_mapping.get('final_comments')),
                'assessments': []
            }
            
            # Extrahera bedömningar
            for i, assessment_area in enumerate(self.assessment_areas, 1):
                grade = self._get_cell_value(row, assessment_area['question_column'])
                comment = self._get_cell_value(row, assessment_area['comment_column']) if assessment_area['comment_column'] else ""
                
                # Extrahera beskrivning från kolumnnamn
                description = self._extract_description_from_column(assessment_area['question_column'])
                
                assessment_data = {
                    'area': f"Område {i}",
                    'description': description,
                    'grade': grade,
                    'comment': comment
                }
                
                student_data['assessments'].append(assessment_data)
            
            return student_data
            
        except Exception as e:
            logger.error(f"Fel vid extraktion av studentdata: {e}")
            return None
    
    def _get_cell_value(self, row, column_name: Optional[str]) -> str:
        """Hämtar cellvärde säkert"""
        if column_name is None or pd.isna(row.get(column_name)):
            return ""
        return str(row[column_name]).strip()
    
    def _extract_description_from_column(self, column_name: str) -> str:
        """Extraherar beskrivning från kolumnnamn"""
        if ':' in column_name:
            # Ta bort Q-nummer och kolon
            description = column_name.split(':', 1)[1].strip()
            # Ta bort radbrytningar och extra mellanslag
            description = ' '.join(description.split())
            return description
        return column_name
    
    def get_structure_summary(self) -> Dict:
        """Returnerar en sammanfattning av den identifierade strukturen"""
        return {
            'basic_columns': self.column_mapping,
            'assessment_areas_count': len(self.assessment_areas),
            'assessment_areas': self.assessment_areas,
            'total_students': len(self.students_data)
        }