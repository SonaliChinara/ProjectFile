//
//  ViewController.swift
//  BMICalculator
//

//

import UIKit

class ViewController: UIViewController, UITextFieldDelegate {

    @IBOutlet var mainView: UIView!
    @IBOutlet weak var heightTextField: UITextField!
    @IBOutlet weak var weightTextField: UITextField!
    
    @IBOutlet weak var bmiLabel: UILabel!
    @IBOutlet weak var riskLabel: UILabel!
    
    var links = [String]()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        
        let tap: UITapGestureRecognizer = UITapGestureRecognizer(target: self, action: #selector(UIInputViewController.dismissKeyboard))
        
        mainView.addGestureRecognizer(tap)
        
        self.heightTextField.delegate = self
        self.weightTextField.delegate = self
        
    }
    

    
    
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        self.view.endEditing(true)
        return false
    }

    @IBAction func calculateBMI(_ sender: UIButton) {
    
        self.view.endEditing(true)
        
        let heightData = heightTextField.text!
        let weightData = weightTextField.text!
        
        let urlString = "http://webstrar99.fulton.asu.edu/page3/Service1.svc/calculateBMI?height=\(heightData)&weight=\(weightData)"

        let url = URL(string: urlString)!

        let urlSession = URLSession.shared

        let jsonQuery = urlSession.dataTask(with: url, completionHandler: { data, response, error -> Void in

            let decoder = JSONDecoder()
            let jsonResult = try! decoder.decode(bmiResults.self, from: data!)

            let bmiValue = jsonResult.bmi
            let moreLink = jsonResult.more
            let riskFactor = jsonResult.risk

            let bmiRes = String(format: "%.1f", bmiValue)
            let riskRes = riskFactor

            self.links = moreLink

            DispatchQueue.main.async {
                self.bmiLabel.text = bmiRes
                self.riskLabel.text = riskRes
                self.riskLabel.textColor = self.getColor(bmi: bmiValue)
            }

        })

        jsonQuery.resume()
        
    }
    
    func getColor(bmi: Float) -> UIColor {
        
        if (bmi < 18) {
            return UIColor.blue
        }
        else if (bmi >= 18 && bmi < 25) {
            return UIColor.green
        }
        else if (bmi >= 25 && bmi < 30) {
            return UIColor.purple
        }
        else {
            return UIColor.red
        }
    }
    
    @IBAction func educate(_ sender: UIButton) {
        
        self.view.endEditing(true)
        
        if (self.links.count > 0) {
            let numLinks = (self.links.count) - 1
            
            guard let moreUrl = URL(string: self.links[Int.random(in: 0..<numLinks)]) else { return }
            UIApplication.shared.open(moreUrl)
        }
        
        else {
            self.riskLabel.text = "Calculate BMI first"
            self.riskLabel.textColor = UIColor.yellow
        }
        
    }
    
}

