import sys
from pathlib import Path
import logging

# Add backend directory to sys.path so 'app' imports work
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from app.core.logging import setup_logging
from app.ml.evaluation import CrossOperatorValidator

logger = logging.getLogger(__name__)

def main():
    setup_logging()
    
    # The dataset structure is typically extracted as something like:
    # data/external/cross_op/PNEUMONIA-radiography-dataset/NORMAL and PNEUMONIA
    # or just data/external/cross_op/NORMAL and PNEUMONIA
    
    cross_op_root = PROJECT_ROOT / "data" / "external" / "cross_op"
    
    # We want to run validation on the 'test' split which contains exactly 485 samples
    dataset_path = cross_op_root / "Radiography" / "test"
                
    if not dataset_path.exists():
        logger.error("Could not find NORMAL and PNEUMONIA folders in %s", cross_op_root)
        sys.exit(1)
        
    logger.info("Found cross-operator dataset at: %s", dataset_path)
    
    validator = CrossOperatorValidator(dataset_path=str(dataset_path))
    results = validator.run()
    
    print("\n" + "="*50)
    print(" 🏥 CROSS-OPERATOR VALIDATION COMPLETE")
    print("="*50)
    print(f" Samples Evaluated: {results['cross_operator_samples']}")
    print(f" Accuracy:          {results['cross_operator_accuracy']*100:.1f}%")
    print(f" Sensitivity:       {results['cross_operator_sensitivity']*100:.1f}%")
    print(f" Specificity:       {results['cross_operator_specificity']*100:.1f}%")
    print(f" Precision:         {results['cross_operator_precision']*100:.1f}%")
    print(f" F1 Score:          {results['cross_operator_f1']:0.3f}")
    print(f" ROC AUC:           {results['cross_operator_roc_auc']:0.3f}")
    print("="*50)

if __name__ == "__main__":
    main()
