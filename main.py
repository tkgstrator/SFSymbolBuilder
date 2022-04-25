import os
import datetime

build_time = datetime.datetime.now().strftime("%Y/%m/%d")

headers = """//  SFSymbol.swift
//  SFSymbol
//
//  Created by Shiota Kyotaro on BUILD_TIME.
//  Copyright © 2022 Magi Corporation. All rights reserved.
//

import Foundation
import SwiftUI

public enum SFSymbol: String {
"""

headers = headers.replace("BUILD_TIME", build_time)


footers = """}

extension SFSymbol: Identifiable, Codable {
    public var id: String { rawValue }
}

extension Image {
    public init(systemName: SFSymbol) {
        self.init(systemName: systemName.rawValue)
    }
}
"""

availables = {
    "130": [13.0, 11.0, 6.0],
    "131": [13.1, 11.0, 6.1],
    "140": [14.0, 11.0, 7.0],
    "142": [14.2, 11.0, 7.1],
    "145": [14.5, 11.0, 7.4],
    "150": [15.0, 12.0, 8.0],
    "151": [15.1, 12.1, 8.1],
    "152": [15.2, 12.1, 8.3],
    "154": [15.4, 12.3, 8.5],
}

if __name__=="__main__":
    versions = sorted(os.listdir("versions"))
    with open("SFSymbol.swift", mode="w") as w:
        w.write(headers)
        for version in versions:
            with open(f"versions/{version}", mode="r") as f:
                lines = f.readlines()
                available = availables[version[:3]]
                version_text = f"@available(iOS {available[0]}, macOS {available[1]}, tvOS {available[0]}, watchOS {available[2]}, *)"
                for line in lines:
                    orig_text = line.strip()
                    if line[0].isdigit():
                        enum_text = "SF"+"".join(list(map(lambda x: x.capitalize() ,line.strip().split("."))))
                    else:
                        enum_text = "".join(list(map(lambda x: x.capitalize() ,line.strip().split("."))))
                    swift_text = f"\t{version_text} case {enum_text} = \"{orig_text}\"\n"
                    w.write(swift_text)
        w.write(footers)
