import UIKit
import CoreLocation
import SystemConfiguration.CaptiveNetwork

class WifiSignalViewController: UIViewController, CLLocationManagerDelegate {

    var compassNeedle: UIView!
    var rssiLabel: UILabel!
    let locationManager = CLLocationManager()

    override func viewDidLoad() {
        super.viewDidLoad()

        view.backgroundColor = .white

        // Set up compass needle
        compassNeedle = UIView(frame: CGRect(x: view.frame.size.width / 2 - 2, y: view.frame.size.height / 2 - 100, width: 4, height: 100))
        compassNeedle.backgroundColor = .red
        view.addSubview(compassNeedle)

        // Set up RSSI label
        rssiLabel = UILabel(frame: CGRect(x: 20, y: view.frame.size.height - 50, width: view.frame.size.width - 40, height: 50))
        rssiLabel.textAlignment = .center
        rssiLabel.text = "RSSI: N/A"
        view.addSubview(rssiLabel)

        // Set up location manager
        locationManager.delegate = self
        locationManager.startUpdatingHeading()

        updateSignalStrength()
    }

    func updateSignalStrength() {
        guard let interface = getConnectedWifiInterface() else {
            rssiLabel.text = "No connected wireless interface found"
            return
        }

        if let rssi = getRSSI(interface: interface) {
            rssiLabel.text = "RSSI: \(rssi) dBm"
            let angle = calculateDirection(rssi: rssi)
            updateNeedle(angle: angle)
        } else {
            rssiLabel.text = "Failed to retrieve RSSI"
        }

        DispatchQueue.main.asyncAfter(deadline: .now() + 2.0) {
            self.updateSignalStrength()
        }
    }

    func calculateDirection(rssi: Int) -> CGFloat {
        if rssi > -50 {
            return 0
        } else if rssi > -60 {
            return 45
        } else if rssi > -70 {
            return 90
        } else if rssi > -80 {
            return 135
        } else {
            return 180
        }
    }

    func updateNeedle(angle: CGFloat) {
        let radians = angle * .pi / 180
        UIView.animate(withDuration: 0.5) {
            self.compassNeedle.transform = CGAffineTransform(rotationAngle: radians)
        }
    }

    func getConnectedWifiInterface() -> String? {
        if let interfaces = CNCopySupportedInterfaces() as? [String] {
            for interface in interfaces {
                if let info = CNCopyCurrentNetworkInfo(interface as CFString) as NSDictionary? {
                    if let ssid = info[kCNNetworkInfoKeySSID as String] as? String {
                        return ssid
                    }
                }
            }
        }
        return nil
    }

    func getRSSI(interface: String) -> Int? {
        if let interfaces = CNCopySupportedInterfaces() as? [String] {
            for interface in interfaces {
                if let info = CNCopyCurrentNetworkInfo(interface as CFString) as NSDictionary? {
                    if let rssi = info[kCNNetworkInfoKeyRSSI as String] as? Int {
                        return rssi
                    }
                }
            }
        }
        return nil
    }

    func locationManager(_ manager: CLLocationManager, didUpdateHeading newHeading: CLHeading) {
        let angle = CGFloat(newHeading.magneticHeading)
        updateNeedle(angle: angle)
    }

    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        locationManager.startUpdatingHeading()
    }

    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        locationManager.stopUpdatingHeading()
    }
}
